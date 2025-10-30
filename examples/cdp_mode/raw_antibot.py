from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/antibot/login"
    sb.activate_cdp_mode(url)
    sb.press_keys("input#username", "demo_user")
    sb.press_keys("input#password", "secret_pass")
    sb.click("button#myButton")
    sb.sleep(1.5)
    sb.click("a#log-in")
    sb.assert_text("Welcome!", "h1")
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
    sb.sleep(1.5)
