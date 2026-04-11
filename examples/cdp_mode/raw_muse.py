"""(Bypasses Friendly Captcha)"""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://muse.jhu.edu/verify"
    sb.activate_cdp_mode(url)
    sb.sleep(1.5)
    sb.solve_captcha()
    sb.sleep(4)
    sb.assert_element('#search_input')
    sb.sleep(3)
