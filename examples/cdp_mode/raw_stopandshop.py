"""Test Stop & Shop search. Non-US IPs might be blocked."""
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://stopandshop.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.6)
    if not sb.is_element_present("#brand-logo_link"):
        sb.refresh()
        sb.sleep(2.6)
        sb.wait_for_element("#brand-logo_link", timeout=3)
    query = "Fresh Turkey"
    required_text = "Turkey"
    search_box = 'input[type="search"]'
    sb.wait_for_element(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, query)
    sb.sleep(1.2)
    sb.click("button.search-btn")
    sb.sleep(3.2)
    print('*** Stop & Shop Search for "%s":' % query)
    print('    (Results must contain "%s".)' % required_text)
    print('    (Results cannot contain "Out of Stock")')
    unique_item_text = []
    item_selector = "div.product-tile_content"
    items = sb.find_elements(item_selector)
    for item in items:
        sb.sleep(0.06)
        if "Out of Stock" not in item.text:
            if required_text in item.text:
                item.flash(color="44CC88")
                sb.sleep(0.025)
                if item.text not in unique_item_text:
                    unique_item_text.append(item.text)
                    print("* " + item.text)
