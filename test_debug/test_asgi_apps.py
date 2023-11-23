from typing import AsyncGenerator, Generator

import httpx
import pytest
from fastapi import FastAPI
from flask import Flask
from httpx import AsyncClient, Client


def fastapi_app():
    app = FastAPI()

    @app.get("/hello")
    async def hello():
        return {"message": "Hello World"}

    return app


def flask_app() -> Flask:
    app = Flask(__name__)

    @app.route("/hello")
    def hello():
        return {"message": "Hello World"}

    return app


@pytest.mark.asyncio
@pytest.fixture(scope="session")
async def fastapi_client_test() -> AsyncGenerator[AsyncClient, None]:
    async with httpx.AsyncClient(base_url="http://test", app=fastapi_app()) as client:
        yield client


@pytest.mark.asyncio
async def test_hello_route_fastapi(fastapi_client_test: AsyncClient):
    response = await fastapi_client_test.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.fixture(scope="session")
def flask_client_test() -> Generator[Client, None, None]:
    with Client(base_url="http://test", app=flask_app()) as client:
        yield client


def test_hello_route_flask(flask_client_test: Client):
    response = flask_client_test.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
