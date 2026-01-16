from seleniumbase import SB

with SB(uc=True, test=True, locale="en", guest=True, ad_block=True) as sb:
    url = "https://www.priceline.com"
    sb.activate_cdp_mode(url)
    sb.sleep(1.8)
    sb.click('input[name="endLocation"]')
    sb.sleep(1.2)
    location = "Portland, OR"
    selection = "Oregon, United States"  # (Dropdown option)
    sb.press_keys('input[name="endLocation"]', location)
    sb.sleep(0.5)
    sb.click_if_visible('input[name="endLocation"]')
    sb.sleep(0.5)
    sb.click(selection)
    sb.scroll_down(25)
    sb.click_if_visible('button[aria-label="Dismiss calendar"]')
    sb.click_if_visible("div.sidebar-iframe-close")
    sb.click_if_visible('div[aria-label="Close Modal"]')
    sb.click('button[data-testid="HOTELS_SUBMIT_BUTTON"]')
    sb.sleep(4.8)
    if len(sb.cdp.get_tabs()) > 1:
        sb.cdp.close_active_tab()
        sb.cdp.switch_to_newest_tab()
        sb.sleep(0.6)
    sb.sleep(0.8)
    for y in range(1, 9):
        sb.scroll_to_y(y * 400)
        sb.sleep(0.5)
    hotel_names = sb.find_elements('a[data-autobot-element-id*="HOTEL_NAME"]')
    if sb.is_element_visible('[font-size="4,,,5"]'):
        hotel_prices = sb.find_elements('[font-size="4,,,5"]')
    else:
        hotel_prices = sb.find_elements(
            '[font-size="12px"] + [font-size="20px"]'
        )
    print("Priceline Hotels in %s:" % location)
    print(sb.get_text('[data-testid="POPOVER-DATE-PICKER"]'))
    if len(hotel_names) == 0:
        print("No availability over the selected dates!")
    count = 0
    for i, hotel in enumerate(hotel_names):
        if hotel_prices[i] and hotel_prices[i].text:
            count += 1
            hotel_price = "$" + hotel_prices[i].text
            print("* %s: %s => %s" % (count, hotel.text, hotel_price))
