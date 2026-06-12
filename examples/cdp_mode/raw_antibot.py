"""CDP Mode bypasses bot-detection and performs stealthy actions.
sb.press_keys() is a slower sb.type() for human-like speed."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://seleniumbase.io/antibot/login")
    sb.press_keys("input#username", "demo_user")
    sb.type("input#password", "secret_pass")
    sb.click("button#myButton")
    sb.sleep(1.4)
    sb.click("a#log-in")
    sb.assert_text("Welcome!", "h1")
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
