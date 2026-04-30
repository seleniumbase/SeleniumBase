"""An example of clicking at custom CAPTCHA coordinates."""
from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://secure.indeed.com/auth"
    sb.activate_cdp_mode(url)
    sb.sleep(1.8)
    sb.solve_captcha()
    sb.sleep(1.8)
    sb.type('input[type="email"]', "test@test.com")
    sb.sleep(1.5)
    sb.click('button[type="submit"]')
    sb.sleep(3.2)
    sb.solve_captcha()
    sb.sleep(4.5)
