"""SB Manager using CDP Mode for bypassing CAPTCHAs."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://wsform.com/demo/")
    sb.sleep(2)
    sb.solve_captcha()
    sb.sleep(3)
