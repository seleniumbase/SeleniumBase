from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.uc_open_with_disconnect("nopecha.com/demo/turnstile", 3.5)
    sb.uc_gui_press_keys("\t\t ")
    sb.sleep(3.5)
    sb.connect()
    sb.uc_gui_handle_cf("#example-container5 iframe")

    if sb.is_element_visible("#example-container0 iframe"):
        sb.switch_to_frame("#example-container0 iframe")
        sb.assert_element("circle.success-circle")
        sb.switch_to_parent_frame()

    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!", duration=3)
