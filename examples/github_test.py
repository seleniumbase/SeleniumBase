from seleniumbase import BaseCase


class GitHubTests(BaseCase):
    def test_github(self):
        # Selenium can trigger GitHub's anti-automation system:
        # "You have triggered an abuse detection mechanism."
        # "Please wait a few minutes before you try again."
        # To avoid this automation blocker, two steps are being taken:
        # 1. self.slow_click() is being used to slow down Selenium actions.
        # 2. The browser's User Agent is modified to avoid Selenium-detection
        #    when running in headless mode on Chrome or Edge (Chromium).
        if self.headless and (
            self.browser == "chrome" or self.browser == "edge"
        ):
            self.get_new_driver(
                agent="""Mozilla/5.0 """
                """AppleWebKit/537.36 (KHTML, like Gecko) """
                """Chrome/92.0.4515.159 Safari/537.36"""
            )
        self.open("https://github.com/search?q=SeleniumBase")
        self.slow_click('a[href="/seleniumbase/SeleniumBase"]')
        self.click_if_visible('[data-action="click:signup-prompt#dismiss"]')
        self.assert_element("div.repository-content")
        self.assert_text("SeleniumBase", "h1")
        self.slow_click('a[title="seleniumbase"]')
        self.slow_click('a[title="fixtures"]')
        self.slow_click('a[title="base_case.py"]')
        self.assert_text("Code", "nav a.selected")
