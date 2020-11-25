from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_contains_selector(self):
        self.open("https://xkcd.com/2207/")
        self.assert_text("Math Work", "#ctitle")
        self.click('a:contains("Next")')
        self.assert_text("Drone Fishing", "#ctitle")
