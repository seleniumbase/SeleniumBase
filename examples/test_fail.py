""" This test was made to fail on purpose to demonstrate the
    logging capabilities of the SeleniumBase Test Framework """

import pytest
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    @pytest.mark.expected_failure
    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        print("\n(This test fails on purpose)")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)
