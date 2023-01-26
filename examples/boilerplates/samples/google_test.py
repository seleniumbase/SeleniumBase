"""google.com example test that uses page objects"""
from seleniumbase import BaseCase
from .google_objects import HomePage, ResultsPage


class GoogleTests(BaseCase):
    def test_google_dot_com(self):
        self.open("https://google.com/ncr")
        self.sleep(0.5)
        self.hide_elements('iframe[name="callout"]')
        self.save_screenshot_to_logs()  # ("./latest_logs" folder)
        self.type(HomePage.search_box, "github.com")
        self.assert_element(HomePage.search_button)
        self.assert_element(HomePage.feeling_lucky_button)
        self.click(HomePage.search_button)
        self.assert_text("github.com", ResultsPage.search_results)
