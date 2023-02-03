"""Uses the SeleniumBase implementation of HTML-Inspector to inspect the HTML.
See https://github.com/philipwalton/html-inspector for more details.
(Only works on Chrome and Chromium-based browsers.)"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class HtmlInspectorTests(BaseCase):
    def test_html_inspector(self):
        self.open("https://xkcd.com/1144/")
        self.inspect_html()
