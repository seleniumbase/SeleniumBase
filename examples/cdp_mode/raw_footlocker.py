from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.footlocker.com/")
    sb.click_if_visible('button[id*="Agree"]', timeout=3)
    sb.click('input[name="query"]')
    search = "Nike Shoes"
    sb.press_keys('input[name="query"]', search)
    sb.sleep(1.2)
    sb.click('ul[id*="typeahead"] li div')
    sb.sleep(3.5)
    elements = sb.select_all("a[data-productcard]")
    if elements:
        print('**** Found results for "%s": ****' % search)
    else:
        print('**** No results found for "%s". ****' % search)
    for element in elements:
        print("------------------ >>>")
        print("* " + element.text)
