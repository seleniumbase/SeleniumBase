from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", ad_block=True)
sb.goto("https://www.footlocker.com/")
sb.click_if_visible('button[id*="Agree"]', timeout=3)
sb.click('input[name="query"]')
search = "Nike Shoes"
sb.press_keys('input[name="query"]', search)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    input_field = 'input[name="query"]'
    sb.sleep(1.2)
    page.click('ul[id*="typeahead"] li div')
    sb.sleep(3.5)
    items = page.locator("a[data-productcard]")
    count = items.count()
    if count:
        print('**** Found results for "%s": ****' % search)
    else:
        print('**** No results found for "%s". ****' % search)
    for i in range(items.count()):
        print("------------------ >>>")
        print("* " + items.nth(i).inner_text().replace("\n", " "))
