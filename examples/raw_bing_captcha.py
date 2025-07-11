from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.bing.com/turing/captcha/challenge"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.uc_gui_click_captcha()
    sb.sleep(1)
