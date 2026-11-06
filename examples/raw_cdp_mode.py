"""Bypass bot-detection with SeleniumBase CDP Mode."""
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
sb.click("input#autologin")
sb.solve_captcha()
sb.assert_element('input[name="login"]')
sb.assert_element_not_visible("input[disabled]")
sb.sleep(1)

sb.goto("https://gitlab.com/users/sign_in")
sb.sleep(2)
sb.solve_captcha()
sb.highlight('h1:contains("GitLab")')
sb.highlight('button:contains("Sign in")')
sb.quit()
