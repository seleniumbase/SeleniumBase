from seleniumbase import BaseCase
from parameterized import parameterized


class GoogleTestClass(BaseCase):

    @parameterized.expand([
        ["pypi", "https://pypi.org"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["seleniumbase", "https://github.com/seleniumbase/SeleniumBase"],
    ])
    def test_parameterized_google_search(self, search_term, expected_url):
        self.open('https://google.com')
        self.update_text('input[title="Search"]', search_term + '\n')
        self.assert_text(expected_url, '#search')
