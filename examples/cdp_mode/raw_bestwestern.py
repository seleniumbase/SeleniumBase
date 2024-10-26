from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.bestwestern.com/en_US.html"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible("div.onetrust-close-btn-handler")
    sb.sleep(1)
    sb.cdp.click("input#destination-input")
    sb.sleep(2)
    location = "Palm Springs, CA, USA"
    sb.cdp.press_keys("input#destination-input", location)
    sb.sleep(1)
    sb.cdp.click("ul#google-suggestions li")
    sb.sleep(1)
    sb.cdp.click("button#btn-modify-stay-update")
    sb.sleep(4)
    sb.cdp.click("label#available-label")
    sb.sleep(2.5)
    print("Best Western Hotels in %s:" % location)
    summary_details = sb.cdp.get_text("#summary-details-column")
    dates = summary_details.split("ROOM")[0].split("DATES")[-1].strip()
    print("(Dates: %s)" % dates)
    flip_cards = sb.cdp.select_all(".flipCard")
    for i, flip_card in enumerate(flip_cards):
        hotel = flip_card.query_selector(".hotelName")
        price = flip_card.query_selector(".priceSection")
        if hotel and price:
            print("* %s: %s => %s" % (
                i + 1, hotel.text.strip(), price.text.strip())
            )
