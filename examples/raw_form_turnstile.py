from seleniumbase import SB


def open_the_form_turnstile_page(sb):
    sb.driver.uc_open_with_reconnect(
        "https://seleniumbase.io/apps/form_turnstile", reconnect_time=2.27,
    )


def click_turnstile_and_verify(sb):
    sb.driver.uc_switch_to_frame("iframe")
    sb.driver.uc_click("span.mark")
    sb.highlight("img#captcha-success", timeout=3.33)


with SB(uc=True, test=True) as sb:
    open_the_form_turnstile_page(sb)
    try:
        click_turnstile_and_verify(sb)
    except Exception:
        open_the_form_turnstile_page(sb)
        click_turnstile_and_verify(sb)
    sb.press_keys("#name", "SeleniumBase")
    sb.press_keys("#email", "test@test.test")
    sb.press_keys("#phone", "1-555-555-5555")
    sb.click('[for="date"]')
    sb.click("td.is-today button")
    sb.click('div[class="select-wrapper"] input')
    sb.click('span:contains("9:00 PM")')
    sb.highlight_click('input[value="AR"] + span')
    sb.click('input[value="cc"] + span')
    sb.highlight_click('button:contains("Request & Pay")')
    sb.highlight("img#submit-success")
    sb.highlight('button:contains("Success!")')
