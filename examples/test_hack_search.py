""" Testing the "self.set_attribute()" and "self.set_attributes()" methods
    to modify a Google search into becoming a Bing search.
    set_attribute() -> Modifies the attribute of the first matching element.
    set_attributes() -> Modifies the attribute of all matching elements. """
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class HackingTests(BaseCase):
    def test_hack_search(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            print("\n  Skipping test in headless mode.")
            self.skip('Skipping test in headless mode.')
        self.open("https://google.com/ncr")
        self.hide_elements("iframe")
        self.assert_element('[title="Search"]')
        self.sleep(0.5)
        self.set_attribute('[action="/search"]', "action", "//bing.com/search")
        self.set_attributes('[value="Google Search"]', "value", "Bing Search")
        self.type('[title="Search"]', "GitHub SeleniumBase Docs Install")
        self.sleep(0.5)
        self.js_click('[value="Bing Search"]')
        self.highlight("h1.b_logo", loops=8)
        self.highlight_click('[href*="github.com/seleniumbase/SeleniumBase"]')
        self.highlight_click('[href="/seleniumbase/SeleniumBase"]')
        self.assert_text("SeleniumBase", "strong a")
        self.highlight("strong a")
        self.js_click('a[title="examples"]')
        self.highlight('#repo-content-turbo-frame')
        self.js_click('a[title="test_hack_search.py"]')
        self.assert_text("test_hack_search.py", "#file-name-id-wide")
        self.highlight("#file-name-id-wide")
