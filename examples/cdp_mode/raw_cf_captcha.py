from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://wsform.com/demo/")
    sb.sleep(2.5)
    sb.solve_captcha()
    sb.sleep(3)
