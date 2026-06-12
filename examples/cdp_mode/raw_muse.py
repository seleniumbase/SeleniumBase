"""(Bypasses Friendly Captcha)"""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://muse.jhu.edu/verify")
    sb.sleep(1.6)
    sb.solve_captcha()
    sb.sleep(4)
    sb.assert_element('#search_input')
    sb.sleep(3)
