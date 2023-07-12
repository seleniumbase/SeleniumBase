from pprint import pformat
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--uc", "--uc-cdp", "--incognito", "-s"])


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
        self.sleep(2)

    def fail_me(self):
        self.fail('Selenium was detected! Try using: "pytest --uc"')

    def test_display_cdp_events(self):
        if not (self.undetectable and self.uc_cdp_events and self.incognito):
            self.get_new_driver(
                undetectable=True, uc_cdp_events=True, incognito=True
            )
        self.add_cdp_listener()
        self.open("https://nowsecure.nl/#relax")
        try:
            self.verify_success()
        except Exception:
            self.clear_all_cookies()
            self.get_new_driver(devtools=True)
            self.add_cdp_listener()
            self.open("https://nowsecure.nl/#relax")
            try:
                self.verify_success()
            except Exception:
                self.fail_me()
