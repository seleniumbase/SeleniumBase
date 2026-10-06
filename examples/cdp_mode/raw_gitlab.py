from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://gitlab.com/users/sign_in")
    sb.sleep(2)
    sb.solve_captcha()
    sb.highlight('h1:contains("GitLab")')
    sb.highlight('button:contains("Sign in")')
