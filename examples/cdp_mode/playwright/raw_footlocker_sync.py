from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", ad_block=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.footlocker.com/")
    input_field = 'input[name="query"]'
    page.wait_for_selector(input_field)
    sb.sleep(1.5)
    sb.click_if_visible('button[id*="Agree"]')
    sb.sleep(1.2)
    page.click(input_field)
    sb.sleep(0.5)
    search = "Nike Shoes"
    sb.press_keys(input_field, search)
    sb.sleep(1.2)
    page.click('ul[id*="typeahead"] li div')
    sb.sleep(3.5)
    elements = sb.select_all("a.ProductCard-link")
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("------------------ >>>")
        print("* " + element.text)
    sb.sleep(2)
