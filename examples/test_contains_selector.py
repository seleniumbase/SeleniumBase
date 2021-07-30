from seleniumbase import BaseCase


class ContainsSelectorTests(BaseCase):
    def test_contains_selector(self):
        self.open("https://xkcd.com/2207/")
        self.assert_element('div.box div:contains("Math Work")')
        self.click('a:contains("Next")')
        self.assert_element('div div:contains("Drone Fishing")')
