"""Verify if your browser is detectable by anti-bot services.
To evade detection, add --uc as a pytest command-line option.
UC + CDP Mode is used: CDP Mode is activated from UC Mode."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class UndetectedTest(BaseCase):
    def test_browser_is_undetected(self):
        self.activate_cdp_mode()  # If not UC Mode, then 2nd browser
        self.goto("https://gitlab.com/users/sign_in")
        self.sleep(2)
        self.solve_captcha()  # (Only runs when a CAPTCHA is visible)
        self.assert_text("Username", '[for="user_login"]', timeout=3)
        self.post_message("SeleniumBase wasn't detected", duration=4)
        self._print("\n Success: SeleniumBase wasn't detected! ")
