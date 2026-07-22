from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.easyjet.com/en/")
    sb.sleep(1.8)
    sb.click_if_visible("button#ensRejectAds", timeout=2)
    sb.sleep(1)
    input_from = 'input[name="from"]'
    sb.click(input_from)
    sb.sleep(1)
    sb.clear(input_from)
    sb.press_keys(input_from, "London Gatwick")
    sb.sleep(1)
    sb.click('span[data-testid="airport-name"]')
    sb.sleep(1)
    sb.press_keys('input[name="to"]', "Paris")
    sb.sleep(1)
    sb.click('span[data-testid="airport-name"]')
    sb.sleep(1)
    sb.click('input[name="when"]')
    sb.sleep(1)
    sb.click('[data-testid="month"]:last-of-type [aria-disabled="false"]')
    sb.sleep(1)
    sb.click('[data-testid="month"]:last-of-type [aria-disabled="false"]')
    sb.sleep(1)
    sb.click('button[data-testid="submit"]')
    sb.sleep(4)
    sb.connect()
    sb.sleep(1)
    for window in sb.driver.window_handles:
        sb.switch_to_window(window)
        if "/buy/flights" in sb.get_current_url():
            break
    sb.click_if_visible("button#ensCloseBanner")
    days = sb.find_elements('div[class*="FlightGridLayout_column"]')
    for day in days:
        if not day.text.strip():
            continue
        print("**** " + " ".join(day.text.split("\n")[0:2]) + " ****")
        fares = day.find_elements("css selector", 'button[class*="flightDet"]')
        if not fares:
            print("No flights today!")
        for fare in fares:
            info = fare.text
            info = info.replace("LOWEST FARE\n", "")
            info = info.replace("\n", "  ")
            print(info)
