from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    url = (
        "https://www.gassaferegister.co.uk/gas-safety"
        "/gas-safety-certificates-records/building-regulations-certificate"
        "/order-replacement-building-regulations-certificate/"
    )
    page.goto(url)
    page.wait_for_timeout(600)
    sb.solve_captcha()
    page.wait_for_selector("#SearchTerm")
    page.wait_for_timeout(2000)
    allow_cookies = 'button:contains("Allow all cookies")'
    sb.click_if_visible(allow_cookies, timeout=2)
    page.wait_for_timeout(1000)
    page.fill("#SearchTerm", "Hydrogen")
    sb.click_if_visible(allow_cookies, timeout=1)
    page.click("button.search-button")
    page.wait_for_timeout(3000)
    items = page.locator("div.search-result")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print(item_text.replace("\n\n", "\n") + "\n")
    sb.scroll_to_bottom()
    page.wait_for_timeout(3000)
