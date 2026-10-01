from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("www.planetminecraft.com/account/sign_in/")
sb.solve_captcha()
sb.wait_for_element_absent("input[disabled]")
sb.sleep(2)
