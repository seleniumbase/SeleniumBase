"""This test is only for Microsoft Edge (Chromium)!"""
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--edge", "-s"])


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
        self.highlight('div[role="main"]')
        self.highlight('img[srcset*="logo"]')
        self.assert_text("Microsoft Edge", 'img[srcset*="logo"] + div')
        self.highlight('img[srcset*="logo"] + div span:nth-of-type(1)')
        self.highlight('img[srcset*="logo"] + div span:nth-of-type(2)')
        if self.is_element_visible('span[aria-live="assertive"]'):
            self.highlight('span[aria-live="assertive"]', loops=8)
        elif self.is_element_visible('a[href*="fwlink"]'):
            self.highlight('a[href*="fwlink"]', loops=8)
        self.highlight('a[href*="chromium"]')
        self.highlight('a[href*="credits"]')
