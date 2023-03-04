from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class GitHubTests(BaseCase):
    def test_github(self):
        if self.headless or self.page_load_strategy == "none":
            self.open_if_not_url("about:blank")
            message = "Unsupported mode for this test."
            print("\n  " + message)
            self.skip(message)
        self.open("https://github.com/search?q=SeleniumBase")
        self.slow_click('a[href="/seleniumbase/SeleniumBase"]')
        self.click_if_visible('[data-action="click:signup-prompt#dismiss"]')
        self.highlight("div.Layout-main")
        self.highlight("div.Layout-sidebar")
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "strong a")
        self.click('a[title="seleniumbase"]')
        self.slow_click('a[title="fixtures"]')
        self.assert_element('a[title="base_case.py"]')
