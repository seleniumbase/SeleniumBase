from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "seleniumbase.io/apps/turnstile"
    sb.uc_open_with_reconnect(url, reconnect_time=2)
    sb.uc_gui_handle_cf()
    sb.assert_element("img#captcha-success", timeout=3)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)
