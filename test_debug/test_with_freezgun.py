from datetime import datetime

import freezegun
import pytest
from pytest_mock import MockFixture


def return_some_object_with_iso_datetime() -> dict[str, str]:
    return {"requested_at": datetime.now().isoformat(), "value": "some value"}


@pytest.mark.xfail(reason="The 'requested_at' field is not the same as time moves")
def test_return_some_object_with_iso_datetime_failing():
    assert return_some_object_with_iso_datetime() == {
        "requested_at": datetime.now().isoformat(),
        "value": "some value",
    }


def test_return_some_object_with_iso_datetime_with_any(mocker: MockFixture) -> None:
    """
    Here we will use mocker special variable ANY.
    ANY will be equal to anything that is passed to it.
    """
    assert return_some_object_with_iso_datetime() == {
        "requested_at": mocker.ANY,
        "value": "some value",
    }


@freezegun.freeze_time("2021-01-01")
def test_return_some_object_with_iso_datetime_with_freezegun() -> None:
    """
    Here we will use freezegun.
    Freezegun will freeze the time to the date we pass to it.
    So we can make this test deterministic.
    """
    assert return_some_object_with_iso_datetime() == {
        "requested_at": "2021-01-01T00:00:00",
        "value": "some value",
    }
