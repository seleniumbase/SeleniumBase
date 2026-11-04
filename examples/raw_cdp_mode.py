"""Bypass bot-detection with SeleniumBase CDP Mode.
Assert statements that aren't met raise exceptions.
"""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()  # Launches a stealth browser
sb.goto("https://browserscan.net/bot-detection")
sb.assert_element('strong:contains("Normal")')
sb.sleep(1)

sb.goto("https://bot.sannysoft.com/")
sb.assert_element(".passed")
sb.assert_element_not_visible(".failed")
sb.sleep(1)

sb.goto("https://www.planetminecraft.com/account")
sb.type('[name="email"]', "Test123")
sb.type('[name="password"]', "Pass")
sb.click("input#autologin")  # Unchecks a checkbox
sb.solve_captcha()  # (as backup if not automatic)
sb.assert_element('input[name="login"]')
sb.assert_element_not_visible("input[disabled]")
sb.sleep(1)  # (only to slow down the live demo)
sb.quit()  # (otherwise quits automatically at end)
