from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.uc_open_with_reconnect("nopecha.com/demo/turnstile", 3.2)
    if sb.is_element_visible("#example-container0"):
        sb.uc_gui_click_captcha("#example-container0")
    sb.uc_gui_click_captcha("#example-container5")
    sb.sleep(3)
