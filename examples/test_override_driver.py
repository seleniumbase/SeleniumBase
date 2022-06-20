from selenium import webdriver
from seleniumbase import BaseCase


class OverrideDriverTest(BaseCase):
    def get_new_driver(self, *args, **kwargs):
        """This method overrides get_new_driver() from BaseCase."""
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        if self.headless:
            options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def test_simple(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_text("Demo Page", "h1")
