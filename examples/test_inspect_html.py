"""
Uses the SeleniumBase implementation of HTML-Inspector to inspect the HTML.
See https://github.com/philipwalton/html-inspector for more details.
(Only works on Chrome and Chromium-based browsers.)
"""

from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_html_inspector(self):
        self.open("https://xkcd.com/1144/")
        self.inspect_html()
