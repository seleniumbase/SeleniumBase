from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.hyatt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.cdp.click_if_visible('button[aria-label="Close"]')
    sb.sleep(1)
    sb.cdp.click('span:contains("Explore")')
    sb.sleep(1)
    sb.cdp.click('a:contains("Hotels & Resorts")')
    sb.sleep(3)
    location = "Anaheim, CA, USA"
    sb.cdp.press_keys("input#searchbox", location)
    sb.sleep(1)
    sb.cdp.click("div#suggestion-list ul li a")
    sb.sleep(1)
    sb.cdp.click('div.hotel-card-footer button')
    sb.sleep(1)
    sb.cdp.click('button[data-locator="find-hotels"]')
    sb.sleep(5)
    hotel_names = sb.cdp.select_all(
        'div[data-booking-status="BOOKABLE"] [class*="HotelCard_header"]'
    )
    hotel_prices = sb.cdp.select_all(
        'div[data-booking-status="BOOKABLE"] div.rate'
    )
    sb.assert_true(len(hotel_names) == len(hotel_prices))
    print("Hyatt Hotels in %s:" % location)
    print("(" + sb.cdp.get_text("ul.b-color_text-white") + ")")
    if len(hotel_names) == 0:
        print("No availability over the selected dates!")
    for i, hotel in enumerate(hotel_names):
        print("* %s: %s => %s" % (i + 1, hotel.text, hotel_prices[i].text))
