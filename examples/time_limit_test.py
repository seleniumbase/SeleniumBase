import pytest
from seleniumbase import BaseCase
from seleniumbase import decorators
BaseCase.main(__name__, __file__)


class TimeLimitTests(BaseCase):
    @pytest.mark.expected_failure
    def test_runtime_limit_decorator(self):
        """This test fails on purpose to show the runtime_limit() decorator
        for code blocks that run longer than the time limit specified."""
        print("\n(This test should fail)")
        self.open("https://xkcd.com/2511")
        with decorators.runtime_limit(0.7):
            self.sleep(0.95)

    @pytest.mark.expected_failure
    def test_set_time_limit_method(self):
        """This test fails on purpose to show the set_time_limit() method
        for tests that run longer than the time limit specified (seconds).
        The time-limit clock starts after the browser has fully launched,
        which is after pytest starts it's own internal clock for tests.
        Usage: (inside tests) =>  self.set_time_limit(SECONDS)
        Usage: (command-line) =>  --time-limit=SECONDS"""
        self.set_time_limit(2.2)  # Fail test if time exceeds 2.2 seconds
        print("\n(This test should fail)")
        self.open("https://xkcd.com/1658")
        self.sleep(3)
