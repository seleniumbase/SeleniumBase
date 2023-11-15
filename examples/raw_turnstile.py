from seleniumbase import SB


def open_the_turnstile_page(sb):
    sb.driver.uc_open_with_reconnect(
        "https://seleniumbase.io/apps/turnstile", reconnect_time=2.27,
    )


def click_turnstile_and_verify(sb):
    sb.driver.uc_switch_to_frame("iframe")
    sb.driver.uc_click("span.mark")
    sb.assert_element("img#captcha-success", timeout=3.33)


with SB(uc=True, test=True) as sb:
    open_the_turnstile_page(sb)
    try:
        click_turnstile_and_verify(sb)
    except Exception:
        open_the_turnstile_page(sb)
        click_turnstile_and_verify(sb)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("Selenium wasn't detected!", duration=3)
