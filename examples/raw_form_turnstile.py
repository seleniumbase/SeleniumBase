from seleniumbase import SB


def click_turnstile_and_verify(sb):
    sb.driver.reconnect(0.1)
    iframe = sb.driver.find_element("iframe")
    sb.driver.reconnect(0.5)
    sb.driver.switch_to.frame(iframe)
    sb.driver.uc_click("span.mark")
    sb.highlight("img#captcha-success", timeout=3.33)


with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect(
        "https://seleniumbase.io/apps/form_turnstile",
        reconnect_time=2.33,
    )
    try:
        click_turnstile_and_verify(sb)
    except Exception:
        sb.driver.uc_open_with_reconnect(
            "https://seleniumbase.io/apps/form_turnstile",
            reconnect_time=2.33,
        )
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
