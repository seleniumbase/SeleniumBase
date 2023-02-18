from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class SearchTests(BaseCase):
    @parameterized.expand(
        [
            ["SeleniumBase Commander", "Commander", "GUI / Commander"],
            ["SeleniumBase Recorder", "Recorder", "Recorder Mode"],
            ["SeleniumBase Syntax", "Syntax", "Syntax Formats"],
        ]
    )
    def test_parameterized_search(self, search_term, keyword, title_text):
        self.open("https://seleniumbase.io/help_docs/how_it_works/")
        self.type('input[aria-label="Search"]', search_term)
        self.click('mark:contains("%s")' % keyword)
        self.assert_title_contains(title_text)
