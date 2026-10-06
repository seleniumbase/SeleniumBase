from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
sb.goto("www.planetminecraft.com/account/sign_in")
sb.solve_captcha()
# "LOG IN" is enabled when the CAPTCHA is bypassed
sb.wait_for_element_absent("input[disabled]")
sb.sleep(2)
sb.quit()
