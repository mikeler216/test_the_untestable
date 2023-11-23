import httpx
import motor
import pytest
import pytest_httpx
import pytest_mock
import requests
from mongomock_motor import AsyncMongoMockClient


def make_a_request_using_requests() -> requests.Response:
    """
    Make a request using requests.
    """
    return requests.get("http://localhost:3000/").json()


def test_make_a_request_using_requests(requests_mock):
    requests_mock.get("http://localhost:3000/", json={"value": "hello mom"})
    assert make_a_request_using_requests() == {"value": "hello mom"}


async def make_a_async_request_using_httpx() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        return await client.get("http://localhost:3000/")


@pytest.mark.asyncio
async def test_make_a_async_request_using_httpx(httpx_mock: pytest_httpx.HTTPXMock):
    httpx_mock.add_response(url="http://localhost:3000/", json={"value": "hello mom"})
    response = await make_a_async_request_using_httpx()
    assert response.json() == {"value": "hello mom"}


async def add_data_to_mongodb(motor_client: motor.MotorClient):
    """
    Make an entire to mongodb.
    """
    db = motor_client.test
    collection = db.test_collection
    await collection.insert_one({"test": "test"})


@pytest.fixture
def async_motor_client():
    return AsyncMongoMockClient()


@pytest.mark.asyncio
async def test_make_an_entire_to_mongodb(
    async_motor_client: AsyncMongoMockClient, mocker: pytest_mock.MockerFixture
):
    await add_data_to_mongodb(motor_client=async_motor_client)
    assert await async_motor_client.test.test_collection.find().to_list() == [
        {"_id": mocker.ANY, "test": "test"}
    ]
