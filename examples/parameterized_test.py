from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class SearchTests(BaseCase):
    @parameterized.expand(
        [
            ["site:Python.org Download", "Download Python", "img.python-logo"],
            ["site:SeleniumBase.io", "SeleniumBase", 'img[alt*="SeleniumB"]'],
            ["site:Wikipedia.org", "Wikipedia", "img.central-featured-logo"],
        ]
    )
    def test_parameterized_search(self, search_key, expected_text, img):
        self.open("https://duckduckgo.com/")
        self.type('input[name="q"]', search_key + "\n")
        self.assert_text(expected_text, "div.results")
        self.click('a:contains("%s")' % expected_text)
        self.assert_element(img)
