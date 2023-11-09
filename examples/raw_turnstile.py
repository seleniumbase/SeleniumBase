from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect(
        "https://seleniumbase.io/apps/turnstile",
        reconnect_time=2.33,
    )
    sb.driver.reconnect(0.1)
    iframe = sb.driver.find_element("iframe")
    sb.driver.reconnect(0.5)
    sb.driver.switch_to.frame(iframe)
    sb.driver.uc_click("span.mark")
    sb.switch_to_default_content()
    sb.assert_element("img#captcha-success", timeout=3.33)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("Selenium wasn't detected!", duration=3)
