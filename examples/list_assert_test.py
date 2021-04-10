""" * Asserting that multiple elements are present or visible:
HTML Presence: assert_elements_present()
HTML Visibility: assert_elements() <> assert_elements_visible()
"""
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_assert_list_of_elements(self):
        self.open("https://store.xkcd.com/collections/posters")
        self.assert_elements_present("head", "style", "script")
        self.assert_elements("h1", "h2", "h3")
        my_list = ["#top-menu", "#col-main", "#col-widgets"]
        self.assert_elements(my_list)
