from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("platform.tavus.io/auth/sign-in?is_developer=true")
sb.sleep(3)
sb.solve_captcha()
sb.sleep(1)
sb.assert_element('input[type="email"]')
sb.assert_element('button[type="submit"]')
