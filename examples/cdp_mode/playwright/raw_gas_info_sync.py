from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    url = (
        "https://www.gassaferegister.co.uk/gas-safety"
        "/gas-safety-certificates-records/building-regulations-certificate"
        "/order-replacement-building-regulations-certificate/"
    )
    page.goto(url)
    sb.sleep(0.6)
    sb.solve_captcha()
    page.wait_for_selector("#SearchTerm")
    sb.sleep(1.4)
    allow_cookies = 'button:contains("Allow all cookies")'
    sb.click_if_visible(allow_cookies, timeout=2)
    sb.sleep(1)
    page.fill("#SearchTerm", "Hydrogen")
    page.click("button.search-button")
    sb.sleep(3)
    items = page.locator("div.search-result")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print(item_text.replace("\n\n", "\n") + "\n")
    sb.scroll_to_bottom()
    sb.sleep(1)
