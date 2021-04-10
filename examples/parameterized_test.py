from seleniumbase import BaseCase
from parameterized import parameterized


class GoogleTests(BaseCase):

    @parameterized.expand([
        ["PyPI", "pypi.org", 'img[alt="PyPI"]'],
        ["Wikipedia", "wikipedia.org", "div#p-logo"],
        ["SeleniumBase", "seleniumbase/SeleniumBase", 'img[title*="Selenium"]']
    ])
    def test_parameterized_google_search(self, search_key, expected_text, img):
        self.open('https://google.com/ncr')
        self.type('input[title="Search"]', search_key + '\n')
        self.assert_element('#result-stats')
        self.assert_text(expected_text, '#search')
        self.click('a:contains("%s")' % expected_text)
        self.assert_element(img)
        self.click(img)
        if "Selenium" in img:
            self.click('img[alt="SeleniumBase.io Docs"]')
            self.assert_element('[title="SeleniumBase Docs"]')
            self.click('a:contains("Features List")')
            self.assert_text("Features List", "h1")
