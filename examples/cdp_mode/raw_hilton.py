from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.hilton.com/en/"
    sb.activate_cdp_mode(url)
    sb.sleep(4.5)
    location = "Sunnyvale, CA, USA"
    location_input = "input#location-input"
    sb.wait_for_element(location_input)
    sb.sleep(1.2)
    sb.click("input#location-input")
    sb.sleep(1.2)
    sb.press_keys("input#location-input", location)
    sb.sleep(2)
    sb.click('span:contains("Check-in")')
    sb.sleep(1.2)
    sb.click('button[aria-current="date"]')
    sb.sleep(1.2)
    sb.click('button[data-testid="shop-modal-done-cta"]')
    sb.sleep(1.5)
    sb.click('button[data-testid="search-submit-button"]')
    sb.sleep(6.5)
    sb.reconnect()
    for window in sb.driver.window_handles:
        sb.switch_to_window(window)
        if "/search/" in sb.get_current_url():
            break
    hotel_card = 'li[data-testid*="hotel-card"]'
    hotel_cards = sb.select_all(hotel_card)
    print("Hilton Hotels in %s:" % location)
    if not hotel_cards:
        print("No availability over the selected dates!")
    css = "css selector"  # Reconnected Selenium - Using WebElement API
    for i, card in enumerate(hotel_cards):
        hotel = card.find_element(css, 'h3[data-testid*="PropertyName"]')
        price = card.find_element(css, 'p[data-testid="rateItem"]')
        if hotel and price:
            print("* %s: %s => %s" % (
                i + 1, hotel.text.strip(), price.text.strip())
            )
