""" This test fails on purpose to demonstrate the time-limit feature
    for tests that run longer than the time limit specified in seconds.
    Usage: (inside tests) -> self.set_time_limit(SECONDS) """

import pytest
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    @pytest.mark.expected_failure
    def test_time_limit_feature(self):
        self.set_time_limit(6)  # Test fails if run-time exceeds limit
        self.open("https://xkcd.com/1658/")
        self.sleep(7)
