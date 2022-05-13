from seleniumbase import BaseCase


class GitHubTests(BaseCase):
    def test_github(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            print("\n  This test is NOT designed for Headless Mode!")
            self.skip('Do NOT use "--headless" with this test!')
        self.open("https://github.com/search?q=SeleniumBase")
        self.slow_click('a[href="/seleniumbase/SeleniumBase"]')
        self.click_if_visible('[data-action="click:signup-prompt#dismiss"]')
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "h2 strong")
        self.slow_click('a[title="seleniumbase"]')
        self.slow_click('a[title="fixtures"]')
        self.slow_click('a[title="base_case.py"]')
        self.assert_text("Code", "nav a.selected")
