import re
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "www.elal.com/flight-deals/en-us/flights-from-boston-to-tel-aviv"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.cdp.click('button[data-att="search"]')
    sb.sleep(5)
    sb.cdp.click_if_visible("#onetrust-close-btn-container button")
    sb.sleep(1)
    view_other_dates = 'button[aria-label*="viewOtherDates.cta"]'
    if sb.cdp.is_element_visible(view_other_dates):
        sb.cdp.click(view_other_dates)
        sb.sleep(5)
    if sb.is_element_visible("flexible-search-calendar"):
        print("*** Flight Calendar for El Al (Boston to Tel Aviv): ***")
        print(sb.cdp.get_text("flexible-search-calendar"))
        prices = []
        elements = sb.cdp.find_elements("span.matric-cell__content__price")
        if elements:
            print("*** Prices List: ***")
            for element in elements:
                prices.append(element.text)
            prices.sort(key=lambda x: int(re.sub("[^0-9]", "", x)))
            for price in prices:
                print(price)
            print("*** Lowest Price: ***")
            lowest_price = prices[0]
            print(lowest_price)
            sb.cdp.scroll_down(12)
            sb.sleep(1)
            sb.cdp.find_element_by_text(lowest_price).click()
            sb.sleep(2)
            search_cell = 'button[aria-label*="Search.cell.buttonTitle"]'
            sb.cdp.scroll_into_view(search_cell)
            sb.sleep(1)
            sb.cdp.click(search_cell)
            sb.sleep(5)
    else:
        print("*** Lowest Prices: ***")
        departure_prices = "#uiFlightPanel0 div.ui-bound__price__value"
        return_prices = "#uiFlightPanel1 div.ui-bound__price__value"
        elements = sb.cdp.find_elements(departure_prices)
        for element in elements:
            if "lowest price" in element.text:
                print("Departure Flight:")
                print(element.text)
                break
        elements = sb.cdp.find_elements(return_prices)
        for element in elements:
            if "lowest price" in element.text:
                print("Return Flight:")
                print(element.text)
                break
    dates = sb.cdp.find_elements('div[class*="flight-date"]')
    if len(dates) == 2:
        print("*** Departure Date: ***")
        print(dates[0].text)
        print("*** Return Date: ***")
        print(dates[1].text)
