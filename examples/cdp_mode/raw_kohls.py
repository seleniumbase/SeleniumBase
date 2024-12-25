from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://www.kohls.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    search = "Mickey Mouse 100 friends teal pillow"
    required_text = "Mickey"
    sb.cdp.press_keys('input[name="search"]', search + "\n")
    sb.sleep(5)
    for item in sb.cdp.find_elements("div.products-container-right"):
        if "Sponsored" in item.text:
            item.remove_from_dom()
    sb.cdp.remove_elements("#tce-sticky-wrapper")
    sb.cdp.remove_elements("li.sponsored-product")
    sb.cdp.remove_elements("#tce-dec-ces-3-banner")
    print('*** Kohls Search for "%s":' % search)
    for item in sb.cdp.find_elements("ul.products a img"):
        if item:
            item.flash(color="44CC88")
            title = item.get_attribute("title")
            if title and required_text in title:
                print("* " + title)
                sb.sleep(0.1)
    sb.sleep(1)
