"""TAG:contains("TEXT") is a special, non-standard CSS Selector
that gets converted to XPath: '//TAG[contains(., "TEXT")]'
before it's used by Selenium calls. Also part of jQuery."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ContainsSelectorTests(BaseCase):
    def test_contains_selector(self):
        self.open("https://xkcd.com/2207/")
        self.assert_element('div.box div:contains("Math Work")')
        self.click('a:contains("Next")')
        self.assert_element('div div:contains("Drone Fishing")')
