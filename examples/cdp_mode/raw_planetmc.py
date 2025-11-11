from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "www.planetminecraft.com/account/sign_in/"
    sb.activate_cdp_mode(url)
    sb.sleep(1.2)
    sb.solve_captcha()
    sb.wait_for_element_absent("input[disabled]")
    sb.sleep(2)
