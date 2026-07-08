from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True, ad_block=True)
sb.goto("https://www.zillow.com/")
sb.sleep(2)
search = "Bar Harbor ME homes on the waterfront"
sb.type('input[aria-label="Search"]', search)
sb.sleep(1)
sb.click('button[type="submit"]')
sb.sleep(2)
sb.click_if_visible('span:contains("Cancel")')
sb.sleep(0.5)
sb.click_if_visible('button[title="Close"]')
items = sb.find_visible_elements('[data-testid="property-card"]')
print('*** %s:' % search)
for i, item in enumerate(items):
    print(f"* <====== {i + 1} ======>")
    print(item.query_selector('[data-testid*="details"]').text)
    print(item.query_selector('[data-testid*="address"]').text)
    print(item.query_selector('[data-testid*="price"]').text)
    item.scroll_into_view()
sb.sleep(2)
sb.quit()
