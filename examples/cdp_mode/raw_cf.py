"""Using CDP Mode to bypass CAPTCHAs in different ways."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.uc_gui_handle_captcha()  # PyAutoGUI Tabs + Spacebar
    sb.sleep(3)

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(4)
    sb.uc_gui_click_captcha()  # PyAutoGUI mouse click
    sb.sleep(3)

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(4)
    sb.solve_captcha()  # CDP Input.dispatchMouseEvent
    sb.sleep(3)
