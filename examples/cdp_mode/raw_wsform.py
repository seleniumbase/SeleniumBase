from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://wsform.com/demo/"
    sb.activate_cdp_mode(url)
    sb.scroll_into_view("div.grid")
    sb.uc_gui_click_captcha()
    sb.sleep(1)
