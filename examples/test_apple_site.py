# -*- coding: utf-8 -*-
from seleniumbase import BaseCase


class AppleTestClass(BaseCase):

    def test_apple_developer_site_webdriver_instructions(self):
        self.demo_mode = True
        self.demo_sleep = 0.5
        self.message_duration = 2.0
        if self.headless and (
                self.browser == "chrome" or self.browser == "edge"):
            self.driver.quit()
            self.get_new_driver(
                agent="""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) """
                      """AppleWebKit/537.36 (KHTML, like Gecko) """
                      """Chrome/75.0.3770.100 Safari/537.36""")
        self.open("https://developer.apple.com/search/")
        title = "Testing with WebDriver in Safari"
        self.type('[placeholder*="developer.apple.com"]', title + "\n")
        self.click("link=%s" % title)
        self.assert_element('div.localnav-content [href*="/documentation/"]')
        self.assert_text(title, "h1")
        self.highlight("div.description div.abstract")
        self.highlight("h2")
        h3 = "h3:nth-of-type(%s)"
        self.assert_text("Make Sure You Have Safari’s WebDriver", h3 % "1")
        self.assert_text("Get the Correct Selenium Library", h3 % "2")
        self.assert_text("Configure Safari to Enable WebDriver", h3 % "3")
        self.assert_text("Write a WebDriver Testing Suite", h3 % "4")
        self.assert_text("Run Your Test", h3 % "5")
