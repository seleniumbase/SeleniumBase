from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://secure.indeed.com/auth")
    sb.sleep(2.2)
    if not sb.is_element_visible('input[type="email"]'):
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
