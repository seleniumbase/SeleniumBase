""" Test an error page with the "highlight() command, which uses a
    JavaScript animation to point out page objects that are found.
    If an element isn't visible, the test fails with an exception.
"""
from seleniumbase import BaseCase


class ErrorPageTests(BaseCase):
    def test_error_page(self):
        self.open("https://seleniumbase.io/error_page/")
        self.highlight('img[alt="500 Error"]')
        self.highlight("img#parallax_octocat")
        self.highlight("#parallax_error_text")
        self.highlight('img[alt*="404"]')
        self.highlight("img#octobi_wan_catnobi")
        self.highlight("img#speeder")
