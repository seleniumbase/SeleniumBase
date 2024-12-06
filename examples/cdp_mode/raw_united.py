from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://www.united.com/en/us"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    origin_input = 'input[placeholder="Origin"]'
    origin = "Boston, MA"
    destination_input = 'input[placeholder="Destination"]'
    destination = "San Diego, CA"
    sb.cdp.gui_click_element(origin_input)
    sb.sleep(1.2)
    sb.cdp.type(origin_input, origin)
    sb.sleep(1.2)
    sb.cdp.click('strong:contains("%s")' % origin)
    sb.sleep(1.2)
    sb.cdp.gui_click_element(destination_input)
    sb.sleep(1.2)
    sb.cdp.type(destination_input, destination)
    sb.sleep(1.2)
    sb.cdp.click('strong:contains("%s")' % destination)
    sb.sleep(1.2)
    sb.cdp.click('button[aria-label="Find flights"]')
    sb.sleep(6)
    flights = sb.find_elements('div[class*="CardContainer__block"]')
    print("**** Flights from %s to %s ****" % (origin, destination))
    if not flights:
        print("* No flights found!")
    for flight in flights:
        print("* " + flight.text.split(" Destination")[0])
    sb.sleep(1.5)
