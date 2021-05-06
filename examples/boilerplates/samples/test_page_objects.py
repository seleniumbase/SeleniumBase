""" Example test that uses the Page Object Model """

from seleniumbase import BaseCase


class GooglePage:
    def go_to_google(self, sb):
        sb.open("https://google.com/ncr")

    def do_search(self, sb, search_term):
        sb.type('input[title="Search"]', search_term + "\n")

    def click_search_result(self, sb, content):
        sb.click('a[href*="%s"]' % content)


class SeleniumBaseGitHubPage:
    def click_seleniumbase_io_link(self, sb):
        link = '#readme article a[href*="seleniumbase.io"]'
        sb.wait_for_element_visible(link)
        sb.js_click(link)
        sb.switch_to_newest_window()


class SeleniumBaseIOPage:
    def do_search_and_click(self, sb, search_term):
        if sb.is_element_visible('[for="__search"] svg'):
            sb.click('[for="__search"] svg')
        sb.type('form[name="search"] input', search_term)
        sb.click("li.md-search-result__item h1:contains(%s)" % search_term)


class MyTests(BaseCase):
    def test_page_objects(self):
        search_term = "SeleniumBase GitHub"
        expected_text = "seleniumbase/SeleniumBase"
        GooglePage().go_to_google(self)
        GooglePage().do_search(self, search_term)
        self.assert_text(expected_text, "#search")
        GooglePage().click_search_result(self, expected_text)
        SeleniumBaseGitHubPage().click_seleniumbase_io_link(self)
        SeleniumBaseIOPage().do_search_and_click(self, "Dashboard")
        self.assert_text("Dashboard", "main h1")
