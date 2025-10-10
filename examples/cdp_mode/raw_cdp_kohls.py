from seleniumbase import sb_cdp

url = "https://www.kohls.com/"
sb = sb_cdp.Chrome(url, locale="en", guest=True)
sb.sleep(2.8)
search = "Mickey Mouse 100 friends teal pillow"
required_text = "Mickey"
sb.press_keys('input[name="search"]', search + "\n")
sb.sleep(5)
for item in sb.find_elements("div.products-container-right"):
    if "Sponsored" in item.text:
        item.remove_from_dom()
sb.remove_elements("#tce-sticky-wrapper")
sb.remove_elements("li.sponsored-product")
sb.remove_elements("#tce-dec-ces-3-banner")
print('*** Kohls Search for "%s":' % search)
for item in sb.find_elements("ul.products a img"):
    if item:
        item.flash(color="44CC88")
        title = item.get_attribute("title")
        if title and required_text in title:
            print("* " + title)
            sb.sleep(0.1)
sb.sleep(1)
sb.driver.stop()
