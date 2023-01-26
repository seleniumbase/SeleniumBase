from pprint import pformat
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--uc", "--uc-cdp", "--incognito", "-s"])


class CDPTests(BaseCase):
    def test_display_cdp_events(self):
        if not self.undetectable or not self.uc_cdp_events:
            self.get_new_driver(undetectable=True, uc_cdp_events=True)
        # (To print everything, use "*". Otherwise select specific headers.)
        # self.driver.add_cdp_listener("*", lambda data: print(pformat(data)))
        self.driver.add_cdp_listener(
            "Network.requestWillBeSentExtraInfo",
            lambda data: print(pformat(data))
        )
        self.open("https://nowsecure.nl/#relax")
        self.assert_text("OH YEAH, you passed!", "h1", timeout=7.25)
        self.sleep(2)
