from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.kohls.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.6)
    search = "Mickey Mouse Blanket"
    req_1 = "Mickey"
    req_2 = "Blanket"
    sb.cdp.press_keys('input[name="search"]', search + "\n")
    sb.sleep(5)
    item_selector = 'div[data-testid*="wallet-wrapper"]'
    if not sb.is_element_present(item_selector):
        item_selector = "li.products_grid"
    for item in sb.cdp.find_elements(item_selector):
        if "Sponsored" in item.text:
            item.remove_from_dom()
    sb.cdp.remove_elements("#tce-sticky-wrapper")
    sb.cdp.remove_elements("li.sponsored-product")
    sb.cdp.remove_elements("#tce-dec-ces-3-banner")
    print('*** Kohls Search for "%s":' % search)
    print('    (Results must contain "%s" and "%s".)' % (req_1, req_2))
    title_selector = "div.prod_nameBlock p"
    if not sb.is_element_present(title_selector):
        title_selector = 'a[class*="sm:text"][href*="/product/"]'
    for item in sb.cdp.find_elements(title_selector):
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
