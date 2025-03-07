# An example of bypassing 2 consecutive CF CAPTCHAs"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://sms-man.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
