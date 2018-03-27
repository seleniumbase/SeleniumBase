from seleniumbase import BaseCase


class GitHubTests(BaseCase):

    def test_github(self):
        self.open("https://github.com/")
        self.update_text("input.header-search-input", "SeleniumBase\n")
        self.click('a[href="/seleniumbase/SeleniumBase"]')
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "h1")
        self.click('a[title="seleniumbase"]')
        self.click('a[title="fixtures"]')
        self.click('a[title="base_case.py"]')
        self.assert_text("Code", "nav a.selected")
