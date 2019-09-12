""" This test fails on purpose to demonstrate the timeout feature
    for tests that run longer than the time limit specified. """

import pytest
import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    @pytest.mark.expected_failure
    @pytest.mark.timeout(6)  # The test will fail if it runs longer than this
    def test_timeout_failure(self):
        self.open("https://xkcd.com/1658/")
        time.sleep(7)
