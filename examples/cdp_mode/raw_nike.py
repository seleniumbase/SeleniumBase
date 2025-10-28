from seleniumbase import SB

with SB(uc=True, test=True, locale="en", pls="none") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.click('[data-testid="user-tools-container"] search')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.press_keys('input[type="search"]', search)
    sb.sleep(4)
    details = 'ul[data-testid*="products"] figure .details'
    elements = sb.select_all(details)
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
    sb.sleep(2)
