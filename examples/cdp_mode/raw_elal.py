import datetime
import re
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "www.elal.com/flight-deals/en-us/flights-from-boston-to-tel-aviv"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.click('label:contains("Departure date")')
    sb.sleep(1)
    today = datetime.date.today()
    days_ahead = (4 - today.weekday() + 7) % 7
    next_friday = today + datetime.timedelta(days=days_ahead)
    formatted_date = next_friday.strftime("%m/%d/%Y")
    sb.cdp.gui_click_element('input[aria-describedby*="date-input"]')
    sb.sleep(1)
    sb.cdp.gui_press_keys("\b" * 10 + formatted_date + "\n")
    sb.sleep(1)
    days_ahead = (4 - today.weekday() + 8) % 14
    following_saturday = today + datetime.timedelta(days=days_ahead)
    formatted_date = following_saturday.strftime("%m/%d/%Y")
    sb.cdp.gui_click_element(
        '[data-att="end-date-toggler"] [aria-describedby*="date-input"]'
    )
    sb.sleep(1)
    sb.cdp.gui_press_keys("\b" * 10 + formatted_date + "\n")
    sb.sleep(1)
    sb.click('button[data-att="done"]')
    sb.sleep(1)
    sb.click('button[data-att="search"]')
    sb.sleep(5)
    sb.click_if_visible("#onetrust-close-btn-container button")
    sb.sleep(1)
    view_other_dates = 'button[aria-label*="viewOtherDates.cta"]'
    if sb.is_element_visible(view_other_dates):
        sb.click(view_other_dates)
        sb.sleep(5)
    if sb.is_element_visible("flexible-search-calendar"):
        print("*** Flight Calendar for El Al (Boston to Tel Aviv): ***")
        print(sb.get_text("flexible-search-calendar"))
        prices = []
        elements = sb.find_elements("span.matric-cell__content__price")
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
            sb.scroll_down(12)
            sb.sleep(1)
            sb.find_element_by_text(lowest_price).click()
            sb.sleep(2)
            search_cell = 'button[aria-label*="Search.cell.buttonTitle"]'
            sb.scroll_into_view(search_cell)
            sb.sleep(1)
            sb.click(search_cell)
            sb.sleep(5)
    else:
        print("*** Lowest Prices: ***")
        departure_prices = "#uiFlightPanel0 div.ui-bound__price__value"
        return_prices = "#uiFlightPanel1 div.ui-bound__price__value"
        elements = sb.find_elements(departure_prices)
        for element in elements:
            if "lowest price" in element.text:
                print("Departure Flight:")
                print(element.text)
                break
        elements = sb.find_elements(return_prices)
        for element in elements:
            if "lowest price" in element.text:
                print("Return Flight:")
                print(element.text)
                break
    dates = sb.find_elements('div[class*="flight-date"]')
    if len(dates) == 2:
        print("*** Departure Date: ***")
        print(dates[0].text)
        print("*** Return Date: ***")
        print(dates[1].text)
