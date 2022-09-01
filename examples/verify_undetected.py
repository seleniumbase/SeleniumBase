"""
Determine if your browser is detectable by anti-bot services.
Some sites use scripts to detect Selenium and then block you.
To evade detection, add --uc as a pytest command-line option.
"""
from seleniumbase import BaseCase


class UndetectedTest(BaseCase):
    def test_browser_is_undetected(self):
        self.open("https://nowsecure.nl")
        try:
            self.assert_text("OH YEAH, you passed!", "h1", timeout=6.6)
            self.post_message("Browser wasn't detected!", duration=1.6)
            self._print("\n Success! Website did not detect Selenium!")
        except Exception:
            self.fail('Browser was detected! Try using: "pytest --uc"')
