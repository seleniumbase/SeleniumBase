from pprint import pformat
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "--uc-cdp", "-s")


class CDPTests(BaseCase):
    def add_cdp_listener(self):
        # (To print everything, use "*". Otherwise select specific headers.)
        # self.driver.add_cdp_listener("*", lambda data: print(pformat(data)))
        self.driver.add_cdp_listener(
            "Network.requestWillBeSentExtraInfo",
            lambda data: print(pformat(data))
        )

    def verify_success(self):
        self.assert_text("OH YEAH, you passed!", "h1", timeout=6.25)
        self.sleep(1)

    def fail_me(self):
        self.fail('Selenium was detected! Try using: "pytest --uc"')

    def test_display_cdp_events(self):
        if not (self.undetectable and self.uc_cdp_events):
            self.get_new_driver(undetectable=True, uc_cdp_events=True)
        self.driver.get("https://nowsecure.nl/#relax")
        try:
            self.verify_success()
        except Exception:
            self.clear_all_cookies()
            self.get_new_driver(undetectable=True, uc_cdp_events=True)
            self.driver.get("https://nowsecure.nl/#relax")
            try:
                self.verify_success()
            except Exception:
                if self.is_element_visible('iframe[src*="challenge"]'):
                    with self.frame_switch('iframe[src*="challenge"]'):
                        self.click("span.mark")
                else:
                    self.fail_me()
                try:
                    self.verify_success()
                except Exception:
                    self.fail_me()
        self.add_cdp_listener()
        self.refresh()
        self.sleep(1)
