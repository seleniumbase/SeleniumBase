from rich.pretty import pprint
from seleniumbase import SB


def add_cdp_listener(sb):
    # (To print everything, use "*". Otherwise select specific headers.)
    # self.driver.add_cdp_listener("*", lambda data: print(pformat(data)))
    sb.driver.add_cdp_listener(
        "Network.requestWillBeSentExtraInfo",
        lambda data: pprint(data)
    )


def click_turnstile_and_verify(sb):
    sb.uc_gui_handle_captcha()
    sb.assert_element("img#captcha-success", timeout=3)
    sb.highlight("img#captcha-success", loops=8)


with SB(uc_cdp_events=True, test=True) as sb:
    url = "seleniumbase.io/apps/turnstile"
    sb.uc_open_with_reconnect(url, 2)
    add_cdp_listener(sb)
    click_turnstile_and_verify(sb)
    sb.sleep(1)
    sb.refresh()
    sb.sleep(1.2)
