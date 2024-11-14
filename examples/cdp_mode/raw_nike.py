from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.gui_click_element('div[data-testid="user-tools-container"]')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.cdp.press_keys('input[type="search"]', search)
    sb.sleep(4)
    elements = sb.cdp.select_all('ul[data-testid*="products"] figure .details')
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
    sb.sleep(2)
