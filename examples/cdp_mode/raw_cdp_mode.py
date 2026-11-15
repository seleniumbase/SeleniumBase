"""Bypass bot-detection with SeleniumBase CDP Mode."""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()  # Launch a stealth browser
sb.goto("https://www.planetminecraft.com/account")
sb.type('[name="email"]', "Test123")
sb.type('[name="password"]', "Pass")
sb.click("input#autologin")  # Uncheck a checkbox
sb.solve_captcha()  # (fallback if not automatic)
sb.assert_element('input[name="login"]')
sb.assert_element_not_visible("input[disabled]")
sb.sleep(1)  # (see the live demo more easily)
sb.quit()
