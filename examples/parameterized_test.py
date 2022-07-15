from parameterized import parameterized
from seleniumbase import BaseCase


class GoogleTests(BaseCase):
    @parameterized.expand(
        [
            ["Download Python", "Download Python", "img.python-logo"],
            ["Wikipedia", "www.wikipedia.org", "img.central-featured-logo"],
            ["SeleniumBase.io Docs", "SeleniumBase", 'img[alt*="SeleniumB"]'],
        ]
    )
    def test_parameterized_google_search(self, search_key, expected_text, img):
        self.open("https://google.com/ncr")
        self.hide_elements("iframe")
        self.type('input[title="Search"]', search_key + "\n")
        self.assert_text(expected_text, "#search")
        self.click('a:contains("%s")' % expected_text)
        self.assert_element(img)
        if "SeleniumBase" in search_key:
            self.click('img[alt="SeleniumBase"]')
            self.assert_element('img[title="SeleniumBase"]')
