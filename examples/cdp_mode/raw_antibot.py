from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/antibot/login"
    sb.activate_cdp_mode(url)
    sb.press_keys("input#username", "demo_user")
    sb.press_keys("input#password", "secret_pass")
    x, y = sb.cdp.get_gui_element_center("button#myButton")
    sb.uc_gui_click_x_y(x, y)
    sb.sleep(1.5)
    x, y = sb.cdp.get_gui_element_center("a#log-in")
    sb.uc_gui_click_x_y(x, y)
    sb.assert_text("Welcome!", "h1")
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
    sb.sleep(1.5)
