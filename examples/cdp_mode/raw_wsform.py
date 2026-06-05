"""CDP Mode for bypassing bot-detection & CAPTCHAs.
Note: sb.uc_gui_click_captcha() requires PyAutoGUI,
which is installed automatically if not already."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    url = "https://wsform.com/demo/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.scroll_into_view("div.grid")
    sb.uc_gui_click_captcha()  # PyAutoGUI mouse click
    sb.sleep(2)
