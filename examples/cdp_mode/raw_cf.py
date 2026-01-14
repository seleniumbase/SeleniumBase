"""Using CDP Mode with PyAutoGUI to bypass CAPTCHAs."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.uc_gui_handle_captcha()  # PyAutoGUI press Tab and Spacebar
    sb.sleep(3)

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(4)
    sb.uc_gui_click_captcha()  # PyAutoGUI click. (Linux needs it)
    sb.sleep(3)
