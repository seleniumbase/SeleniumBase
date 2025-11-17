from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    url = "https://wsform.com/demo/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.scroll_into_view("div.grid")
    sb.uc_gui_click_captcha()
    sb.sleep(2)
