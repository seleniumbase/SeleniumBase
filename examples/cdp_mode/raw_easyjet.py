from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.easyjet.com/en/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible('button#ensRejectAll')
    sb.sleep(1.2)
    sb.cdp.click('input[name="from"]')
    sb.sleep(1.2)
    sb.cdp.type('input[name="from"]', "London")
    sb.sleep(1.2)
    sb.cdp.click('span[data-testid="airport-name"]')
    sb.sleep(1.2)
    sb.cdp.type('input[name="to"]', "Venice")
    sb.sleep(1.2)
    sb.cdp.click('span[data-testid="airport-name"]')
    sb.sleep(1.2)
    sb.cdp.click('input[name="when"]')
    sb.sleep(1.2)
    sb.cdp.click('[data-testid="month"] button[aria-disabled="false"]')
    sb.sleep(1.2)
    sb.cdp.click('[data-testid="month"]:last-of-type [aria-disabled="false"]')
    sb.sleep(1.2)
    sb.cdp.click('button[data-testid="submit"]')
    sb.sleep(3.5)
    sb.connect()
    sb.sleep(0.5)
    if "/buy/flights" not in sb.get_current_url():
        sb.driver.close()
    sb.switch_to_newest_window()
    days = sb.find_elements("div.flight-grid-day")
    for day in days:
        print("**** " + " ".join(day.text.split("\n")[0:2]) + " ****")
        fares = day.find_elements("css selector", "button.selectable")
        if not fares:
            print("No flights today!")
        for fare in fares:
            info = fare.text
            info = info.replace("LOWEST FARE\n", "")
            info = info.replace("\n", "  ")
            print(info)
