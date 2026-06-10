from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class GitHubTests(BaseCase):
    def test_github(self):
        if self.headless or self.page_load_strategy == "none":
            self.goto_if_not_url("about:blank")
            print("\n  Unsupported mode for this test.")
            self.skip("Unsupported mode for this test.")
        self.goto("https://github.com/seleniumbase/SeleniumBase")
        self.click_if_visible('[data-action="click:signup-prompt#dismiss"]')
        self.highlight('[class*="PageLayout-Content-"][data-width="large"]')
        self.highlight('[class*="PageLayout-PaneWrapper"]')
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "strong a")
        self.js_click('a[title="seleniumbase"]')
        self.slow_click('td[class*="large"] a[title="fixtures"]')
        self.highlight('td[class*="large"] a[title="base_case.py"]', loops=8)
