from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.hyatt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(3.2)
    sb.click_if_visible('button[aria-label="Close"]')
    sb.sleep(0.1)
    sb.click_if_visible("#onetrust-reject-all-handler")
    sb.sleep(1.2)
    location = "Anaheim, CA, USA"
    sb.type('input[id="search-term"]', location)
    sb.sleep(1.2)
    sb.click('li[data-js="suggestion"]')
    sb.sleep(0.6)
    sb.click_if_visible('button[aria-label="Close"]')
    sb.sleep(0.6)
    sb.click("button.be-button-shop")
    sb.sleep(1)
    sb.click_if_visible('[label="Find Hotels"]')
    sb.sleep(5)
    card_info = 'div[data-booking-status="BOOKABLE"] [class*="HotelCard_info"]'
    hotels = sb.select_all(card_info)
    print("Hyatt Hotels in %s:" % location)
    print("(" + sb.get_text('span[class*="summary_destination"]') + ")")
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
