from seleniumbase import SB

with SB(uc=True, test=True, mobile=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.solve_captcha()
    # (The rest is for testing and demo purposes)
    sb.assert_text("Username", '[for="user_login"]', timeout=3)
    sb.assert_element('label[for="user_login"]')
    sb.highlight('button:contains("Sign in")')
    sb.highlight('h1:contains("GitLab")')
    sb.post_message("SeleniumBase wasn't detected", duration=4)
