from rich.pretty import pprint
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "--uc-cdp", "-s")


class CDPTests(BaseCase):
    def add_cdp_listener(self):
        # (To print everything, use "*". Otherwise select specific headers.)
        # self.driver.add_cdp_listener("*", lambda data: print(pformat(data)))
        self.driver.add_cdp_listener(
            "Network.requestWillBeSentExtraInfo",
            lambda data: pprint(data)
        )

    def verify_success(self):
        self.assert_text("OH YEAH, you passed!", "h1", timeout=6.25)
        self.sleep(1)

    def test_display_cdp_events(self):
        if not (self.undetectable and self.uc_cdp_events):
            self.get_new_driver(undetectable=True, uc_cdp_events=True)
        self.driver.uc_open_with_tab("https://nowsecure.nl/#relax")
        self.verify_success()
        self.add_cdp_listener()
        self.refresh()
        self.sleep(1)
