"""An example of clicking at custom CAPTCHA coordinates."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://secure.indeed.com/auth"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.type('input[type="email"]', "test@test.com")
    sb.sleep(1)
    sb.click('button[type="submit"]')
    sb.sleep(3.5)
    selector = 'div[class*="pass-Captcha"]'
    sb.click_with_offset(selector, 32, 42)
    sb.sleep(4.5)
