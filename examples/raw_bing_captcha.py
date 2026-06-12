from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.bing.com/turing/captcha/challenge")
    sb.sleep(2)
    sb.solve_captcha()
    sb.sleep(2)
