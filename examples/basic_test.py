"""
Same as my_first_test.py, but without the asserts.
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://store.xkcd.com/search")
        self.type('input[name="q"]', "xkcd book\n")
        self.open("https://xkcd.com/353/")
        self.click('a[rel="license"]')
        self.go_back()
        self.click_link_text("About")
