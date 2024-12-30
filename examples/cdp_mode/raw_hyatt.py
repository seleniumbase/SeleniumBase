from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://www.hyatt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible('button[aria-label="Close"]')
    sb.sleep(1)
    sb.cdp.click('span:contains("Explore")')
    sb.sleep(1)
    sb.cdp.click('a:contains("Hotels & Resorts")')
    sb.sleep(3)
    location = "Anaheim, CA, USA"
    sb.cdp.press_keys("input#searchbox", location)
    sb.sleep(2)
    sb.cdp.click("div#suggestion-list ul li a")
    sb.sleep(1)
    sb.cdp.click('div.hotel-card-footer button')
    sb.sleep(1)
    sb.cdp.click('button[data-locator="find-hotels"]')
    sb.sleep(5)
    card_info = 'div[data-booking-status="BOOKABLE"] [class*="HotelCard_info"]'
    hotels = sb.cdp.select_all(card_info)
    print("Hyatt Hotels in %s:" % location)
    print("(" + sb.cdp.get_text("ul.b-color_text-white") + ")")
    if len(hotels) == 0:
        print("No availability over the selected dates!")
    for hotel in hotels:
        info = hotel.text.strip()
        if "Avg/Night" in info and not info.startswith("Rates from"):
            name = info.split("  (")[0].split(" + ")[0].split(" Award Cat")[0]
            name = name.split(" Rates from :")[0]
            price = "?"
            if "Rates from : " in info:
                price = info.split("Rates from : ")[1].split(" Avg/Night")[0]
            print("* %s => %s" % (name, price))
