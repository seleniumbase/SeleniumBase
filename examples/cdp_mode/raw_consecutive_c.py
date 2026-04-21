# An example of bypassing 2 consecutive CF CAPTCHAs"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://agents.moderationinterface.com"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    if not sb.is_element_present("#login-submit"):
        sb.solve_captcha()
        sb.sleep(2)
        sb.wait_for_element("#login-submit", timeout=3)
        sb.sleep(2)
    sb.sleep(1)
    sb.solve_captcha()
    sb.sleep(2)
