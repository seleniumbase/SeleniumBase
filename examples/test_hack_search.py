""" Testing the "self.set_attribute()" and "self.set_attributes()" methods
    to modify a Google search into becoming a Bing search.
    set_attribute() -> Modifies the attribute of the first matching element.
    set_attributes() -> Modifies the attribute of all matching elements. """

from seleniumbase import BaseCase


class HackingTests(BaseCase):
    def test_hack_search(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            print("\n  This test is not for Headless Mode.")
            self.skip('Do not use "--headless" with this test.')
        self.open("https://google.com/ncr")
        self.hide_elements("iframe")
        self.assert_element('input[title="Search"]')
        self.set_attribute('[action="/search"]', "action", "//bing.com/search")
        self.set_attributes('[value="Google Search"]', "value", "Bing Search")
        self.type('input[title="Search"]', "SeleniumBase GitHub Docs Install")
        self.sleep(0.5)
        self.js_click('[value="Bing Search"]')
        self.highlight("h1.b_logo")
        self.highlight_click('[href*="github.com/seleniumbase/SeleniumBase"]')
        self.highlight_click('[href="/seleniumbase/SeleniumBase"]')
        self.highlight_click('a[title="examples"]')
        self.assert_text("examples", "strong.final-path")
        self.highlight_click('a[title="test_hack_search.py"]')
        self.assert_text("test_hack_search.py", "strong.final-path")
        self.highlight("strong.final-path")
