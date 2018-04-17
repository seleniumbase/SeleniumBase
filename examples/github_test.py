from seleniumbase import BaseCase
import time


class GitHubTests(BaseCase):

    # Selenium can trigger GitHub's abuse detection mechanism:
    # "You have triggered an abuse detection mechanism."
    # "Please wait a few minutes before you try again."
    # To avoid this, slow down Selenium actions.
    def slow_click(self, css_selector):
        time.sleep(1)
        self.click(css_selector)

    def test_github(self):
        self.open("https://github.com/")
        self.update_text("input.header-search-input", "SeleniumBase\n")
        self.slow_click('a[href="/seleniumbase/SeleniumBase"]')
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "h1")
        self.slow_click('a[title="seleniumbase"]')
        self.slow_click('a[title="fixtures"]')
        self.slow_click('a[title="base_case.py"]')
        self.assert_text("Code", "nav a.selected")
