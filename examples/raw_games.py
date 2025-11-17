"""SB Manager using CDP Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True, disable_csp=True) as sb:
    url = "https://steamdb.info/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.click("a.header-login span")
    sb.sleep(2)
    sb.solve_captcha()
    sb.assert_text("Sign in", "button#js-sign-in", timeout=4)
    sb.sleep(0.5)
    sb.click("button#js-sign-in")
    sb.sleep(0.5)
    sb.highlight("div.page_content form")
    sb.highlight('button:contains("Sign in")', scroll=False)
    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected", duration=4)
