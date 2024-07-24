from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.bing.com/turing/captcha/challenge"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_click_captcha()
