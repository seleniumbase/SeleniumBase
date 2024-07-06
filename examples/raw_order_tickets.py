from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.thaiticketmajor.com/concert/"
    sb.uc_open_with_reconnect(url, 6.111)
    sb.uc_click("button.btn-signin", 4.1)
    sb.switch_to_frame('iframe[title*="Cloudflare"]')
    if not sb.is_element_visible("svg#success-icon"):
        sb.uc_gui_handle_cf()
        sb.switch_to_frame('iframe[title*="Cloudflare"]')
    sb.assert_element("svg#success-icon")
    sb.switch_to_default_content()
    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!")
