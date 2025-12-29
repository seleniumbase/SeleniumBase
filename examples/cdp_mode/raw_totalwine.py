from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.totalwine.com/"
    sb.activate_cdp_mode()
    sb.open(url)
    sb.sleep(1.8)
    search_box = 'input[data-at="header-search-text"]'
    search = "The Land by Psagot Cabernet"
    if not sb.is_element_present(search_box):
        sb.cdp.evaluate("window.location.reload();")
        sb.sleep(1.8)
    sb.click_if_visible("#onetrust-close-btn-container button")
    sb.sleep(0.5)
    sb.click_if_visible('button[aria-label="Close modal"]')
    sb.sleep(1.2)
    sb.click(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, search)
    sb.sleep(0.6)
    sb.click('button[data-at="header-search-button"]')
    sb.sleep(1.8)
    sb.click('img[data-at="product-search-productimage"]')
    sb.sleep(2.2)
    print('*** Total Wine Search for "%s":' % search)
    print(sb.get_text('h1[data-at="product-name-title"]'))
    print(sb.get_text('span[data-at="product-mix6price-text"]'))
    print("Product Highlights:")
    print(sb.get_text('p[class*="productInformationReview"]'))
    print("Product Details:")
    print(sb.get_text('div[data-at="origin-details-table-container"]'))
