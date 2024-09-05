from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.thaiticketmajor.com/concert/#"
    sb.uc_open_with_reconnect(url, 6.111)
    sb.uc_click("button.btn-signin", 4.1)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
