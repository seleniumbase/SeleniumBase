from seleniumbase import BaseCase


class MultipleDriversTest(BaseCase):
    def test_multiple_drivers(self):
        self.open("data:text/html,<h1>Driver 1</h1>")
        driver2 = self.get_new_driver()
        self.open("data:text/html,<h1>Driver 2</h1>")
        self.switch_to_default_driver()  # Driver 1
        self.highlight("h1")
        self.assert_text("Driver 1", "h1")
        self.switch_to_driver(driver2)  # Driver 2
        self.highlight("h1")
        self.assert_text("Driver 2", "h1")
