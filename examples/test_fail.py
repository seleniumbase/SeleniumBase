""" This test was made to fail on purpose to demonstrate the
    logging capabilities of the SeleniumBase Test Framework """

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.driver.get("http://xkcd.com/731/")
        self.wait_for_element("div#ARMY_OF_ROBOTS", timeout=0.7)
