from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("nopecha.com/demo/turnstile", 3.4)
    if sb.is_element_visible("#example-container0 iframe"):
        sb.switch_to_frame("#example-container0 iframe")
        if not sb.is_element_visible("circle.success-circle"):
            sb.driver.uc_click("span.mark", reconnect_time=3)
            sb.switch_to_frame("#example-container0 iframe")
        sb.switch_to_default_content()

    sb.switch_to_frame("#example-container5 iframe")
    sb.driver.uc_click("span.mark", reconnect_time=2.5)
    sb.switch_to_frame("#example-container5 iframe")
    sb.assert_element("svg#success-icon", timeout=3)
    sb.switch_to_parent_frame()

    if sb.is_element_visible("#example-container0 iframe"):
        sb.switch_to_frame("#example-container0 iframe")
        sb.assert_element("circle.success-circle")
        sb.switch_to_parent_frame()

    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!", duration=3)
