from seleniumbase import BaseCase


class GitHubTests(BaseCase):
    def test_github(self):
        # Selenium can trigger GitHub's anti-automation system:
        # "You have triggered an abuse detection mechanism."
        # "Please wait a few minutes before you try again."
        # To avoid this automation blocker, two steps are being taken:
        # 1. self.slow_click() is being used to slow down Selenium actions.
        # 2. The browser's User Agent is modified to avoid Selenium-detection
        #    when running in headless mode.
        if self.headless:
            self.get_new_driver(
                agent="""Mozilla/5.0 """
                """AppleWebKit/537.36 (KHTML, like Gecko) """
                """Chrome/Version 96.0.4664.55 Safari/537.36"""
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
