""" An example test using the Classic Page Object Model """
from seleniumbase import BaseCase


class GooglePage:
    def go_to_google(self, sb):
        sb.open("https://google.com/ncr")

    def do_search(self, sb, search_term):
        sb.type('input[title="Search"]', search_term + "\n")

    def click_search_result(self, sb, content):
        sb.click('a:contains("%s")' % content)


class SeleniumBaseIOPage:
    def do_search_and_click(self, sb, search_term):
        sb.type('form[name="search"] input', search_term)
        sb.click("li.md-search-result__item h1:contains(%s)" % search_term)


class MyTests(BaseCase):
    def test_page_objects(self):
        search_term = "SeleniumBase.io Docs"
        expected_text = "SeleniumBase"
        GooglePage().go_to_google(self)
        GooglePage().do_search(self, search_term)
        self.assert_text(expected_text, "#search")
        GooglePage().click_search_result(self, expected_text)
        SeleniumBaseIOPage().do_search_and_click(self, "Dashboard")
        self.assert_text("Dashboard", "main h1")
