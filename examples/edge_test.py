"""
This test is only for Microsoft Edge (Chromium)!
"""
from seleniumbase import BaseCase


class EdgeTests(BaseCase):

    def test_edge(self):
        if self.browser != "edge":
            print("\n  This test is only for Microsoft Edge (Chromium)!")
            print('  (Run this test using "--edge" or "--browser=edge")')
            self.skip('Use "--edge" or "--browser=edge"')
        self.open("edge://settings/help")
        self.assert_element('img[alt="Edge logo"] + span')
        self.highlight('#section_about div + div')
        self.highlight('#section_about div + div > div')
        self.highlight('img[alt="Edge logo"]')
        self.highlight('img[alt="Edge logo"] + span')
        self.highlight('#section_about div + div > div + div')
        self.highlight('#section_about div + div > div + div + div > div')
