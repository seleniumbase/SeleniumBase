from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.uc_open_with_reconnect(url)
    sb.uc_gui_click_captcha()  # Only if needed
    sb.assert_element('label[for="user_login"]')
    sb.assert_element('input[data-testid*="username"]')
    sb.assert_element('input[data-testid*="password"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
