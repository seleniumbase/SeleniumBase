from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    window_handle = sb.driver.current_window_handle
    url = "https://www.priceline.com"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.cdp.click('input[name="endLocation"]')
    sb.sleep(1)
    location = "Portland, OR, USA"
    selection = "Oregon, United States"  # (Dropdown option)
    sb.cdp.press_keys('input[name="endLocation"]', location)
    sb.sleep(1)
    sb.click_if_visible('input[name="endLocation"]')
    sb.sleep(1)
    sb.cdp.click("Oregon, United States")
    sb.sleep(1)
    sb.cdp.click('button[aria-label="Dismiss calendar"]')
    sb.sleep(3)
    sb.connect()
    if len(sb.driver.window_handles) > 1:
        sb.switch_to_window(window_handle)
        sb.driver.close()
        sb.sleep(0.1)
        sb.switch_to_newest_window()
        sb.sleep(1)
    hotel_names = sb.find_elements('a[data-autobot-element-id*="HOTEL_NAME"]')
    hotel_prices = sb.find_elements('span[font-size="4,,,5"]')
    print("Priceline Hotels in %s:" % location)
    print(sb.get_text('[data-testid="POPOVER-DATE-PICKER"]'))
    if len(hotel_names) == 0:
        print("No availability over the selected dates!")
    count = 0
    for i, hotel in enumerate(hotel_names):
        if hotel_prices[i] and hotel_prices[i].text:
            count += 1
            print("* %s: %s => %s" % (count, hotel.text, hotel_prices[i].text))
