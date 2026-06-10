from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("www.planetminecraft.com/account/sign_in/")
    sb.sleep(3)
    sb.solve_captcha()
    sb.wait_for_element_absent("input[disabled]")
    sb.sleep(2)
