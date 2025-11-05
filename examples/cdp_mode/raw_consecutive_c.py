# An example of bypassing 2 consecutive CF CAPTCHAs"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://sms-man.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(2.2)
    if not sb.is_element_present('input[name="email"]'):
        sb.solve_captcha()
        sb.sleep(1)
        sb.wait_for_element('[name="email"]', timeout=3)
        sb.sleep(2)
    sb.solve_captcha()
    sb.sleep(2)
