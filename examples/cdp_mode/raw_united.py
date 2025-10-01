from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.united.com/en/us"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    origin_input = 'input[placeholder="Origin"]'
    origin = "New York, NY"
    destination_input = 'input[placeholder="Destination"]'
    destination = "Orlando, FL"
    sb.cdp.gui_click_element(origin_input)
    sb.sleep(0.5)
    sb.cdp.type(origin_input, origin)
    sb.sleep(1.2)
    sb.cdp.click('strong:contains("%s")' % origin)
    sb.sleep(1.2)
    sb.cdp.gui_click_element(destination_input)
    sb.sleep(0.5)
    sb.cdp.type(destination_input, destination)
    sb.sleep(1.2)
    sb.cdp.click('strong:contains("%s")' % destination)
    sb.sleep(1.2)
    sb.cdp.click('button[aria-label="Find flights"]')
    sb.sleep(6)
    flights = sb.find_elements('div[class*="CardContainer__block"]')
    print("**** Flights from %s to %s ****" % (origin, destination))
    print("    (" + sb.get_text("h2.atm-c-heading") + ")")
    if not flights:
        print("* No flights found!")
    for flight in flights:
        flight_info = flight.text.split(" Destination")[0]
        part_1 = flight_info.split(" Departing at")[0]
        part_2 = flight_info.split("Arriving at ")[-1]
        part_2 = part_2.split(" Duration")[0]
        part_3 = flight.text.split(" Destination")[-1].split(" Aircraft")[0]
        parts = "%s - %s %s" % (part_1, part_2, part_3)
        print("* " + parts)
    for category in ["ECONOMY", "ECONOMY-UNRESTRICTED"]:
        prices = sb.find_elements('[aria-describedby="%s"]' % category)
        full_prices = []
        for item in prices:
            item_text = item.text
            if "Not available" not in item.text:
                full_prices.append("$%s" % item.text.split("$")[-1])
            else:
                full_prices.append("N/A")
        print("**** %s Prices:" % category)
        print(full_prices)
    sb.cdp.scroll_down(50)
    sb.sleep(1.5)
