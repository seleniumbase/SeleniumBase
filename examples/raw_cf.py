"""SB Manager using CDP Mode for bypassing CAPTCHAs."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.sleep(4)
    sb.solve_captcha()
    sb.sleep(2.5)
