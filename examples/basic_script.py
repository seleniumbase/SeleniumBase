"""
Same as my_first_test.py, but without the asserts.
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open('http://xkcd.com/353/')
        self.click('a[rel="license"]')
        self.open('http://xkcd.com/1481/')
        self.click("link=Blag")
        self.update_text('input#s', 'Robots!\n')
        self.open('http://xkcd.com/1319/')
