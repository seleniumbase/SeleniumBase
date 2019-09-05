from seleniumbase import BaseCase
from parameterized import parameterized


class GoogleTestClass(BaseCase):

    @parameterized.expand([
        ["pypi", "pypi.org"],
        ["wikipedia", "wikipedia.org"],
        ["seleniumbase", "seleniumbase/SeleniumBase"],
    ])
    def test_parameterized_google_search(self, search_term, expected_text):
        self.open('https://google.com/ncr')
        self.update_text('input[title="Search"]', search_term + '\n')
        self.assert_element('#resultStats')
        self.assert_text(expected_text, '#search')
