""" This test fails on purpose to demonstrate the time-limit feature
    for tests that run longer than the time limit specified (seconds).
    The time-limit clock starts after the browser has fully launched,
    which is after pytest starts it's own internal clock for tests.
    Usage: (inside tests) =>  self.set_time_limit(SECONDS)
    Usage: (command-line) =>  --time-limit=SECONDS """

import pytest
from seleniumbase import BaseCase


class TimeLimitTests(BaseCase):
    @pytest.mark.expected_failure
    def test_time_limit_feature(self):
        self.set_time_limit(5)  # Fail test if time exceeds 5 seconds
        self.open("https://xkcd.com/1658/")
        print("\n(This test should fail)")
        self.sleep(7)
