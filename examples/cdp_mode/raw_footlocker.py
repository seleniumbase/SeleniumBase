from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.footlocker.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible('button[id*="Agree"]')
    sb.sleep(1.5)
    sb.cdp.mouse_click('input[aria-label="Search"]')
    sb.sleep(1.5)
    search = "Nike Shoes"
    sb.cdp.press_keys('input[aria-label="Search"]', search)
    sb.sleep(2)
    sb.cdp.mouse_click('ul[id*="typeahead"] li div')
    sb.sleep(3)
    elements = sb.cdp.select_all("a.ProductCard-link")
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("------------------ >>>")
        print("* " + element.text)
    sb.sleep(2)
