"""An example of clicking at custom CAPTCHA coordinates."""
from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://secure.indeed.com/auth"
    sb.activate_cdp_mode(url)
    sb.sleep(2.2)
    sb.solve_captcha()
    sb.sleep(2.5)
    sb.type('input[type="email"]', "test@test.com")
    sb.sleep(0.5)
    sb.solve_captcha()
    sb.sleep(0.5)
    sb.click('button[type="submit"]')
    sb.sleep(2.5)
    sb.solve_captcha()
    sb.sleep(4.5)
