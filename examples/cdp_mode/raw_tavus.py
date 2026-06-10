from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("platform.tavus.io/auth/sign-in?is_developer=true")
    sb.sleep(3)
    sb.solve_captcha()
    sb.sleep(1)
    sb.assert_element('input[type="email"]')
    sb.assert_element('button[type="submit"]')
