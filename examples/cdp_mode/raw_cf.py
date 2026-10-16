"""Using CDP Mode to bypass CAPTCHAs in different ways.
PyAutoGUI is installed automatically if not already."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://seleniumbase.io/apps/turnstile"
    sb.activate_cdp_mode(url)
    sb.uc_gui_handle_captcha()  # PyAutoGUI Tabs + Spacebar
    sb.sleep(2)

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://seleniumbase.io/apps/turnstile"
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()  # PyAutoGUI mouse click
    sb.sleep(2)

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://seleniumbase.io/apps/turnstile"
    sb.activate_cdp_mode(url)
    sb.solve_captcha()  # CDP Input.dispatchMouseEvent
    sb.sleep(2)
