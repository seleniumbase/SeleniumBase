from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class AppleTests(BaseCase):
    def test_apple_developer_site_webdriver_instructions(self):
        if self.headed:
            self.demo_mode = True
            self.demo_sleep = 0.5
            self.message_duration = 2.0
            if self.is_chromium() and not self.disable_csp:
                self.get_new_driver(browser=self.browser, disable_csp=True)
        if self.headless:
            if self._multithreaded or self.undetectable or self.recorder_mode:
                self.open_if_not_url("about:blank")
                print("\n  Unsupported mode for this test.")
                self.skip("Unsupported mode for this test.")
            elif self.is_chromium():
                self.get_new_driver(browser=self.browser, headless2=True)
        self.open("https://developer.apple.com/search/")
        title = "Testing with WebDriver in Safari"
        self.type('[placeholder*="developer.apple.com"]', title + "\n")
        self.click("link=%s" % title)
        self.assert_element("nav.documentation-nav")
        self.assert_text(title, "h1")
        self.assert_text("Enable WebDriver and run a test.", "div.abstract")
        if self.demo_mode:
            self.highlight("div.content h2")
        else:
            self.assert_element("div.content h2")
        h3 = "div.content h3:nth-of-type(%s)"
        self.assert_text("Make Sure You Have Safari’s WebDriver", h3 % "1")
        self.assert_text("Get the Correct Selenium Library", h3 % "2")
        self.assert_text("Configure Safari to Enable WebDriver", h3 % "3")
        self.assert_text("Write a WebDriver Testing Suite", h3 % "4")
        self.assert_text("Run Your Test", h3 % "5")
