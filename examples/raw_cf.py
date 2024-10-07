"""SB Manager using UC Mode & PyAutoGUI for bypassing CAPTCHAs."""
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.cloudflare.com/login"
    sb.uc_open_with_reconnect(url, 5.5)
    sb.uc_gui_handle_captcha()  # PyAutoGUI press Tab and Spacebar
    sb.sleep(2.5)

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.cloudflare.com/login"
    sb.uc_open_with_reconnect(url, 5.5)
    sb.uc_gui_click_captcha()  # PyAutoGUI click. (Linux needs it)
    sb.sleep(2.5)
