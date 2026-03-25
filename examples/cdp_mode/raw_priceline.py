"""Priceline does a lot of A/B testing. Selectors change frequently."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", guest=True, pls="none") as sb:
    url = "https://www.priceline.com"
    sb.activate_cdp_mode(url)
    sb.sleep(2.6)
    input_selector = '[name="endLocation"]'
    if not sb.is_element_present(input_selector):
        input_selector = "div.location-input input"
    sb.click(input_selector)
    sb.sleep(1.2)
    location = "Portland, OR"
    selection = "Oregon, United States"  # (Dropdown option)
    sb.press_keys(input_selector, location)
    sb.sleep(0.6)
    sb.click(selection)
    sb.sleep(0.4)
    sb.scroll_down(25)
    sb.sleep(0.4)
    calendar_close = 'button[aria-label="Dismiss calendar"]'
    if not sb.is_element_visible(calendar_close):
        calendar_close = '[data-mode="range"] span.px-1'
    sb.click(calendar_close)
    sb.sleep(0.6)
    sb.click('form button[type="submit"]')
    sb.sleep(4.8)
    if len(sb.cdp.get_tabs()) > 1:
        sb.cdp.close_active_tab()
        sb.cdp.switch_to_newest_tab()
        sb.sleep(0.6)
    sb.sleep(0.8)
    for y in range(1, 9):
        sb.scroll_to_y(y * 200)
        sb.sleep(0.4)
    hotel_names = sb.find_elements('h3 div[class*="TitleName"]')
    if not hotel_names:
        hotel_names = sb.find_elements("h3.antialiased")
    price_selector = '[class*="PriceWrap"] .relative > .items-center'
    if sb.is_element_visible(price_selector):
        hotel_prices = sb.find_elements(price_selector)
    elif sb.is_element_present(
        '[font-size="12px"] + [font-size="20px"]'
    ):
        hotel_prices = sb.find_elements(
            '[font-size="12px"] + [font-size="20px"]'
        )
    else:
        hotel_prices = sb.find_elements(
            'span.text-priceSuper-heading4 + div > span'
        )
    print("Priceline Hotels in %s:" % location)
    if len(hotel_names) == 0:
        print("No availability over the selected dates!")
    count = 0
    for i, hotel in enumerate(hotel_names):
        if hotel_prices[i] and hotel_prices[i].text:
            count += 1
            hotel_price = "$" + hotel_prices[i].text
            if hotel_price.startswith("$$ "):
                hotel_price = hotel_price.replace("$$ ", "$")
            print("* %s: %s => %s" % (count, hotel.text, hotel_price))
