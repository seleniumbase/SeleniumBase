"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.driver.uc_open_with_reconnect(url, 3)
    if not sb.is_text_visible("Username", '[for="user_login"]'):
        sb.driver.uc_open_with_reconnect(url, 4)
    sb.assert_text("Username", '[for="user_login"]', timeout=3)
    sb.assert_element('label[for="user_login"]')
    sb.highlight('button:contains("Sign in")')
    sb.highlight('h1:contains("GitLab.com")')
    sb.post_message("SeleniumBase wasn't detected", duration=4)
