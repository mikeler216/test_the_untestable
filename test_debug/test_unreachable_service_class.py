from typing import Never

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


def call_unreachable_service(arguments: list[str]) -> None:
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


def test_call_unreachable_service_with_mock(mock_service):
    # we can assert the call has the params we expect
    # Why is this important? Because we are processing the return value after we call the service.
    # The service is out of our control, but our code is ours, and we have to test it.
    assert mock_service.make_call(["some", "arguments"]) == "some return valu"

    # test that we called the function once
    mock_service.client().call.assert_called_once()

    # test that we called the function with the right arguments
    mock_service.client().call.assert_called_with(["some", "arguments"])




