"""An example of bypassing bot-detection on Southwest.com.
(PyAutoGUI is installed at runtime if it's not installed.)"""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.southwest.com/air/booking/")
    sb.sleep(2.8)
    origin = "DEN"
    destination = "SEA"
    sb.click_if_visible("button#onetrust-accept-btn-handler")
    sb.sleep(0.5)
    sb.gui_click_element("input#originationAirportCode")
    sb.sleep(0.2)
    sb.clear("input#originationAirportCode")
    sb.uc_gui_press_keys(" " + "\n")
    sb.sleep(0.5)
    sb.gui_click_element("input#originationAirportCode")
    sb.sleep(0.5)
    sb.uc_gui_press_keys(origin + "\n")
    sb.sleep(0.5)
    sb.gui_click_element("h1")
    sb.gui_click_element("input#destinationAirportCode")
    sb.sleep(0.2)
    sb.clear("input#destinationAirportCode")
    sb.uc_gui_press_keys(destination + "\n")
    sb.sleep(0.5)
    sb.gui_click_element("h1")
    sb.click_if_visible("button#onetrust-accept-btn-handler")
    sb.sleep(0.1)
    sb.click('form button[data-test="submitField"]')
    sb.sleep(3)
    if sb.is_element_present('button[aria-controls*="DEN-SEA"]'):
        sb.scroll_down(35)
        sb.sleep(0.1)
        sb.gui_click_element('button[aria-controls*="DEN-SEA"]')
    sb.sleep(2.5)
    day = sb.get_text('[aria-selected="true"] span')
    print("**** Flights from %s to %s ****" % (origin, destination))
    flights = sb.find_elements("div[data-flight-id]")
    for flight in flights:
        info = flight.query_selector('[class*="stopsSection"]').text
        if not info:
            continue
        print(f"* {day} -> {info}")
