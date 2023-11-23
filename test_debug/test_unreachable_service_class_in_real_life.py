from typing import Never
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture


class SomeUnreachableService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def client(self) -> Never:
        raise RuntimeError("Service not reachable")

    def make_call(self, arguments: list[str]) -> str:
        """
        Make a call to the service.
        Simple function that calls the service.
        """

        return self.client().call(arguments)[:-1]


def call_unreachable_service_dependency_injection(service: SomeUnreachableService, arguments: list[str]) -> None:
    """
    Call an unreachable service.
    Simple function that calls an unreachable service.
    """
    service.make_call(arguments)


def call_unreachable_service_without_dependency_injection(arguments: list[str]) -> None:
    """
    Call an unreachable service.
    Simple function that calls an unreachable service.
    """
    service = SomeUnreachableService("connection_string")
    service.make_call(arguments)


@pytest.fixture
def mock_service(mocker: MockerFixture):
    _some_unreachable_service_mocked = SomeUnreachableService(connection_string="connection_string")
    _some_unreachable_service_mocked.client = mocker.Mock()

    # we can also add a return value to the mock call
    _some_unreachable_service_mocked.client().call.return_value = "some return value"
    return _some_unreachable_service_mocked


@pytest.fixture
def client_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.MagicMock()


@pytest.fixture
def monkeypatch_service(monkeypatch: pytest.MonkeyPatch, client_mock) -> None:
    """
    Let's try to monkeypatch the service.
    """
    monkeypatch.setattr(SomeUnreachableService, "client", client_mock)


def test_call_unreachable_service_dependency_injection_with_mock(mock_service):
    """
    Now here, where the code uses nice dependency injection, we can test the code without too much hassle.
    We just provide our new mocked service to function, and we can test it.
    """
    call_unreachable_service_dependency_injection(mock_service, ["some", "arguments"])
    # test that we called the function once
    mock_service.client().call.assert_called_once()

    # test that we called the function with the right arguments
    mock_service.client().call.assert_called_with(["some", "arguments"])


def test_call_unreachable_service_without_dependency_injection(monkeypatch_service, client_mock):
    call_unreachable_service_without_dependency_injection(["some", "arguments"])

    # test that we called the function once
    client_mock().call.assert_called_once()

    # test that we called the function with the right arguments
    client_mock().call.assert_called_with(["some", "arguments"])
