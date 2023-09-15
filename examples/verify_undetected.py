"""Determine if your browser is detectable by anti-bot services.
Some sites use scripts to detect Selenium, and then block you.
To evade detection, add --uc as a pytest command-line option."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-s")


class UndetectedTest(BaseCase):
    def verify_success(self):
        self.assert_text("OH YEAH, you passed!", "h1", timeout=6.25)
        self.post_message("Selenium wasn't detected!", duration=2.8)
        self._print("\n Success! Website did not detect Selenium! ")

    def fail_me(self):
        self.fail('Selenium was detected! Try using: "pytest --uc"')

    def test_browser_is_undetected(self):
        if not (self.undetectable):
            self.get_new_driver(undetectable=True)
        self.driver.get("https://nowsecure.nl/#relax")
        try:
            self.verify_success()
        except Exception:
            self.clear_all_cookies()
            self.get_new_driver(undetectable=True)
            self.driver.get("https://nowsecure.nl/#relax")
            try:
                self.verify_success()
            except Exception:
                if self.is_element_visible('iframe[src*="challenge"]'):
                    with self.frame_switch('iframe[src*="challenge"]'):
                        self.click("area")
                else:
                    self.fail_me()
                try:
                    self.verify_success()
                except Exception:
                    self.fail_me()
