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

    def click_turnstile_and_verify(sb):
        sb.uc_gui_handle_captcha()
        sb.assert_element("img#captcha-success", timeout=3)
        sb.highlight("img#captcha-success", loops=8)

    def test_display_cdp_events(self):
        if not (self.undetectable and self.uc_cdp_events):
            self.get_new_driver(undetectable=True, uc_cdp_events=True)
        url = "seleniumbase.io/apps/turnstile"
        self.uc_open_with_reconnect(url, 2)
        self.add_cdp_listener()
        self.click_turnstile_and_verify()
        self.sleep(1)
        self.refresh()
        self.sleep(0.5)
