from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.bing.com/turing/captcha/challenge"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.solve_captcha()
    sb.sleep(2)
