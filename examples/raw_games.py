"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True, disable_csp=True) as sb:
    url = "https://steamdb.info/"
    sb.uc_open_with_reconnect(url, 3)
    sb.uc_click("a.header-login span", 3)
    sb.uc_gui_click_captcha()
    sb.assert_text("Sign in", "button#js-sign-in", timeout=3)
    sb.uc_click("button#js-sign-in", 2)
    sb.highlight("div.page_content form")
    sb.highlight('button:contains("Sign in")', scroll=False)
    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected", duration=4)
