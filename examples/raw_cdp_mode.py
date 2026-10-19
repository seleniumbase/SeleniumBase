"""Bypass bot-detection with SeleniumBase CDP Mode"""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://browserscan.net/bot-detection")
sb.assert_element('strong:contains("Normal")')
sb.sleep(1)

sb.goto("https://bot.sannysoft.com/")
sb.assert_element(".passed")
sb.assert_element_not_visible(".failed")
sb.sleep(1)

sb.goto("https://www.planetminecraft.com/account")
sb.type('[name="email"]', "Name123")
sb.type('[name="password"]', "Pass")
sb.solve_captcha()
sb.assert_element('input[name="login"]')
sb.assert_element_not_visible("input[disabled]")
sb.sleep(1)
sb.quit()
