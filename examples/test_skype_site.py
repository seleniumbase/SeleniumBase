"""
This is a mobile device test for Chromium-based browsers (such as MS Edge)
Usage:  pytest test_skype_site.py --mobile --browser=edge

Default mobile settings for User Agent and Device Metrics if not specified:
        User Agent:   --agent="Mozilla/5.0 (Linux; Android 9; Pixel 3 XL)"
        CSS Width, CSS Height, Pixel-Ratio:   --metrics="411,731,3"
"""
from seleniumbase import BaseCase


class SkypeWebsiteTestClass(BaseCase):

    def test_skype_website_on_mobile(self):
        if not self.mobile_emulator:
            print("\n  This test is only for mobile devices / emulators!")
            print("  (Usage: '--mobile' with a Chromium-based browser.)")
            self.skip("Please rerun this test using '--mobile' !!!")
        self.open("https://www.skype.com/en/")
        self.assert_text("Install Skype", "div.appInfo")
        self.highlight("div.appBannerContent")
        self.highlight('[itemprop="url"]')
        self.highlight("h1")
        self.highlight('[data-bi-area="meet-now-home-page"]')
        self.highlight_click('[data-bi-name="skype-download-home-page"]')
        self.assert_element('[aria-label="Microsoft"]')
        self.assert_text("Download Skype", "h1")
        self.highlight("div.appBannerContent")
        self.highlight("h1")
        self.assert_text("Skype for Mobile", "h2")
        self.highlight("h2")
        self.highlight("#get-skype-0")
        self.highlight_click('[data-bi-name="arrow-dropdown-mobile"]')
        self.highlight('#get-skype-0_android-download')
        self.highlight('[data-bi-id*="ios"]')
        self.highlight('[data-bi-id*="windows10"]')
