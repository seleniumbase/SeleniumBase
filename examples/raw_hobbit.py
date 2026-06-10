from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://seleniumbase.io/hobbit/login")
    sb.click("button span#mySpan")
    sb.assert_text("Welcome to Middle Earth!", "h1")
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
    sb.click("img")
    sb.sleep(5.888)  # Cool animation happening now!
