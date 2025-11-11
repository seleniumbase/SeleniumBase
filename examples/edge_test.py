"""This test is only for Microsoft Edge (Chromium)!"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--edge")


class EdgeTests(BaseCase):
    def test_edge(self):
        if self.browser != "edge":
            self.open_if_not_url("about:blank")
            print("\n  This test is only for Microsoft Edge (Chromium)!")
            print('  (Run this test using "--edge" or "--browser=edge")')
            self.skip('Use "--edge" or "--browser=edge"')
        elif self.headless:
            self.open_if_not_url("about:blank")
            print("\n  This test is NOT designed for Headless Mode!")
            self.skip('Do NOT use "--headless" with this test!')
        self.open("edge://settings/help")
        self.assert_element("app-shell")
        self.assert_text("Microsoft Edge", "app-shell")
        self.sleep(2)
