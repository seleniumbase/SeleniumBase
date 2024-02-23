"""Determine if your browser is detectable by anti-bot services.
Some sites use scripts to detect Selenium, and then block you.
To evade detection, add --uc as a pytest command-line option."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-s")


class UndetectedTest(BaseCase):
    def test_browser_is_undetected(self):
        if not self.undetectable:
            self.get_new_driver(undetectable=True)
        self.driver.uc_open_with_reconnect(
            "https://top.gg/", reconnect_time=4
        )
        if not self.is_text_visible("Discord Bots", "h1"):
            self.get_new_driver(undetectable=True)
            self.driver.uc_open_with_reconnect(
                "https://top.gg/", reconnect_time=5
            )
        self.assert_text("Discord Bots", "h1", timeout=3)
        self.set_messenger_theme(theme="air", location="top_center")
        self.post_message("Selenium wasn't detected!", duration=2.8)
        self._print("\n Success! Website did not detect Selenium! ")
