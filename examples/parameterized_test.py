from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class GoogleTests(BaseCase):
    @parameterized.expand(
        [
            ["site:Python.org Download", "Download Python", "img.python-logo"],
            ["site:SeleniumBase.io", "SeleniumBase", 'img[alt*="SeleniumB"]'],
            ["site:Wikipedia.org", "Wikipedia", "img.central-featured-logo"],
        ]
    )
    def test_parameterized_google_search(self, search_key, expected_text, img):
        self.open("https://google.com/ncr")
        self.remove_elements("iframe")
        self.type('input[title="Search"]', search_key + "\n")
        self.assert_text(expected_text, "#search")
        self.click('a:contains("%s")' % expected_text)
        self.assert_element(img)
