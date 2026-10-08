from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
sb.goto("https://www.planetminecraft.com/account")
sb.assert_element('input[name="login"]')
sb.type('input[name="email"]', "test@example.com")
sb.type('input[name="password"]', "Fake_Password")
sb.click("input#autologin")  # The checkbox
if sb.is_element_visible("input[disabled]"):
    sb.solve_captcha()  # Enables the input button
sb.assert_element_absent("input[disabled]")
sb.sleep(1.5)
sb.quit()
