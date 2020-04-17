"""
This test is only for Microsoft Edge (Chromium)!
"""
from seleniumbase import BaseCase


class EdgeTestClass(BaseCase):

    def test_edge(self):
        if self.browser != "edge":
            print("\n  This test is only for Microsoft Edge (Chromium)!")
            print("  (Run with: '--browser=edge')")
            self.skip("This test is only for Microsoft Edge (Chromium)!")
        self.open("edge://settings/help")
        self.assert_element('img[alt="Edge logo"] + span')
        self.highlight('div[role="main"] div div div + div')
        self.highlight('div[role="main"] div div div + div > div')
        self.highlight('img[alt="Edge logo"]')
        self.highlight('img[alt="Edge logo"] + span')
        self.highlight('div[role="main"] div div div + div > div + div')
        self.highlight('div[role="main"] div div div + div > div + div + div')
