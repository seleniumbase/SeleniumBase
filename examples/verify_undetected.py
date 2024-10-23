"""Determine if your browser is detectable by anti-bot services.
Some sites use scripts to detect Selenium, and then block you.
To evade detection, add --uc as a pytest command-line option."""
from seleniumbase import BaseCase
from seleniumbase import DriverContext
BaseCase.main(__name__, __file__, "--uc", "-s")


class UndetectedTest(BaseCase):
    def test_browser_is_undetected(self):
        url = "https://gitlab.com/users/sign_in"
        if not self.undetectable:
            with DriverContext(uc=True) as driver:
                driver.uc_activate_cdp_mode(url)
                driver.uc_gui_click_captcha()
                driver.assert_text("Username", '[for="user_login"]', timeout=3)
                print("\n Success! Website did not detect Selenium! ")
        else:
            self.activate_cdp_mode(url)
            self.uc_gui_click_captcha()
            self.assert_text("Username", '[for="user_login"]', timeout=3)
            self.post_message("SeleniumBase wasn't detected", duration=4)
            self._print("\n Success! Website did not detect Selenium! ")
