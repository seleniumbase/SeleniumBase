"""
This test is only for Microsoft Edge (Chromium)!
(Tested on Edge Version 96.0.1054.62)
"""
from seleniumbase import BaseCase


class EdgeTests(BaseCase):
    def test_edge(self):
        if self.browser != "edge":
            self.open("data:,")
            print("\n  This test is only for Microsoft Edge (Chromium)!")
            print('  (Run this test using "--edge" or "--browser=edge")')
            self.skip('Use "--edge" or "--browser=edge"')
        if self.headless:
            self.open("data:,")
            print("\n  This test is NOT designed for Headless Mode!")
            self.skip('Do NOT use "--headless" with this test!')
        self.open("edge://settings/help")
        self.highlight('div[role="main"]')
        self.highlight('img[srcset*="logo"]')
        self.assert_text("Microsoft Edge", 'img[srcset*="logo"] + div')
        self.highlight('img[srcset*="logo"] + div span:nth-of-type(1)')
        self.highlight('img[srcset*="logo"] + div span:nth-of-type(2)')
        self.highlight('span[aria-live="assertive"]')
        self.highlight('a[href*="chromium"]')
