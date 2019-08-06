"""
Same as my_first_test.py, but without the asserts.
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.click('a[rel="license"]')
        self.open("https://xkcd.com/1481/")
        self.click("link=Store")
        self.update_text("input#top-search-input", "xkcd book\n")
        self.open("https://xkcd.com/1319/")
