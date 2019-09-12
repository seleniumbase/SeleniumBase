"""
Same as my_first_test.py, but without the asserts.
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.click('a[rel="license"]')
        self.go_back()
        self.click("link=About")
        self.open("https://store.xkcd.com/collections/everything")
        self.update_text("input.search-input", "xkcd book\n")
