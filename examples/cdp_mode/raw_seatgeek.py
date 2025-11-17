from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://seatgeek.com/"
    sb.activate_cdp_mode(url)
    input_field = 'input[name="search"]'
    sb.wait_for_element(input_field)
    sb.sleep(1.6)
    query = "Jerry Seinfeld"
    sb.press_keys(input_field, query)
    sb.sleep(1.6)
    sb.click("li#active-result-item")
    sb.sleep(4.2)
    print('*** SeatGeek Search for "%s":' % query)
    item_selector = '[data-testid="listing-item"]'
    for item in sb.find_elements(item_selector):
        print(item.text)
