from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.footlocker.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.click_if_visible('button[id*="Agree"]')
    sb.sleep(1.5)
    sb.click('input[name="query"]')
    sb.sleep(1.5)
    search = "Nike Shoes"
    sb.press_keys('input[name="query"]', search)
    sb.sleep(2.5)
    sb.click('ul[id*="typeahead"] li div')
    sb.sleep(3.5)
    elements = sb.select_all("a.ProductCard-link")
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("------------------ >>>")
        print("* " + element.text)
    sb.sleep(2)
