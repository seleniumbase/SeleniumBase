"""google.com example test that uses page objects"""
from seleniumbase import BaseCase
try:
    from .google_objects import HomePage, ResultsPage
except Exception:
    from google_objects import HomePage, ResultsPage
    BaseCase.main(__name__, __file__)


class GoogleTests(BaseCase):
    def test_google_dot_com(self):
        if self.headless and self._multithreaded:
            self.open_if_not_url("about:blank")
            print("\n  Skipping test in headless multi-threaded mode.")
            self.skip("Skipping test in headless multi-threaded mode.")
        self.open("https://google.com/ncr")
        self.assert_title_contains("Google")
        self.sleep(0.05)
        self.save_screenshot_to_logs()  # ("./latest_logs" folder)
        if not self.is_element_visible("iframe"):
            self.sleep(1.5)  # A slow pop-up might appear
        self.hide_elements('iframe')  # Hide "Sign in" pop-up
        self.sleep(0.05)
        self.save_screenshot_to_logs()
        self.type(HomePage.search_box, "github.com")
        self.assert_element(HomePage.search_button)
        self.assert_element(HomePage.feeling_lucky_button)
        self.click(HomePage.search_button)
        self.assert_text("github.com", ResultsPage.search_results)
