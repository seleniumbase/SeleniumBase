"""CDP Mode for bypassing bot-detection & CAPTCHAs."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://wsform.com/demo/")
    sb.sleep(2)
    sb.scroll_into_view('form[method="POST"]')
    sb.solve_captcha()
    sb.sleep(2)
