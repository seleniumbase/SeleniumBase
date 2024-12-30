from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://www.easyjet.com/en/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible("button#ensCloseBanner")
    sb.sleep(1.2)
    sb.cdp.click('input[name="from"]')
    sb.sleep(1.2)
    sb.cdp.type('input[name="from"]', "London")
    sb.sleep(0.6)
    sb.cdp.click_if_visible("button#ensCloseBanner")
    sb.sleep(0.6)
    sb.cdp.click('span[data-testid="airport-name"]')
    sb.sleep(1.2)
    sb.cdp.type('input[name="to"]', "Venice")
    sb.sleep(1.2)
    sb.cdp.click('span[data-testid="airport-name"]')
    sb.sleep(1.2)
    sb.cdp.click('input[name="when"]')
    sb.sleep(1.2)
    sb.cdp.click('[data-testid="month"]:last-of-type [aria-disabled="false"]')
    sb.sleep(1.2)
    sb.cdp.click('[data-testid="month"]:last-of-type [aria-disabled="false"]')
    sb.sleep(1.2)
    sb.cdp.click('button[data-testid="submit"]')
    sb.sleep(4.2)
    sb.connect()
    sb.sleep(1.2)
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
