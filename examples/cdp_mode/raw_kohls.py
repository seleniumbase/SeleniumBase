from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    url = "https://www.kohls.com/"
    sb.activate_cdp_mode(url, ad_block=True)
    sb.sleep(2.6)
    search = "Mickey Mouse Blanket"
    req_1 = "Mickey"
    req_2 = "Blanket"
    if not sb.is_element_present('input[name="search"]'):
        sb.refresh()
        sb.sleep(2.6)
    sb.press_keys('input[name="search"]', search + "\n")
    sb.sleep(5)
    item_selector = 'div[data-testid*="wallet-wrapper"]'
    if not sb.is_element_present(item_selector):
        item_selector = "li.products_grid"
    for item in sb.find_elements(item_selector):
        if "Sponsored" in item.text:
            item.remove_from_dom()
    sb.remove_elements("#tce-sticky-wrapper")
    sb.remove_elements("li.sponsored-product")
    sb.remove_elements("#tce-dec-ces-3-banner")
    print('*** Kohls Search for "%s":' % search)
    print('    (Results must contain "%s" and "%s".)' % (req_1, req_2))
    title_selector = "div.prod_nameBlock p"
    if not sb.is_element_present(title_selector):
        title_selector = 'a[class*="sm:text"][href*="/product/"]'
    for item in sb.find_elements(title_selector):
        if item:
            item.flash(color="44CC88")
            title = item.text
            if title:
                if (
                    req_1.lower() in title.lower()
                    and req_2.lower() in title.lower()
                ):
                    print("* " + title)
                    sb.sleep(0.1)
    sb.sleep(1)
