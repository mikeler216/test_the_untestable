from typing import Generator

import pytest


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class CountCalls(metaclass=Singleton):
    call_count = 0

    def __init__(self):
        ...

    def make_call(self):
        self.call_count += 1


# def test_count_calls():
#     count_calls = CountCalls()
#     count_calls.make_call()
#     count_calls.make_call()
#     assert count_calls.call_count == 2
#
#
# def test_failing_test():
#     count_calls = CountCalls()
#     count_calls.make_call()
#     count_calls.make_call()
#     assert count_calls.call_count == 2


@pytest.fixture
def call_count_with_teardown() -> Generator[CountCalls, None, None]:
    """
    This fixture will be called before and after each test that uses it.
    The yield statement is where the test will be run. After the yield statement, the teardown statement will be run.
    This is similar to how "@contextlib.contextmanager" works.
    """
    _count_calls = CountCalls()
    yield _count_calls
    _count_calls.call_count = 0


def test_count_calls_1(call_count_with_teardown):
    call_count_with_teardown.make_call()
    call_count_with_teardown.make_call()
    assert call_count_with_teardown.call_count == 2


def test_not_failing_test(call_count_with_teardown):
    call_count_with_teardown.make_call()
    call_count_with_teardown.make_call()
    assert call_count_with_teardown.call_count == 2
