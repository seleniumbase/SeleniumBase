from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.solve_captcha()
    # (The rest is for testing and demo purposes)
    sb.assert_element('label[for="user_login"]')
    sb.assert_element('input[data-testid*="username"]')
    sb.assert_element('input[data-testid*="password"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
