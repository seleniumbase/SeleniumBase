"""(Bypasses the DataDome slider CAPTCHA)"""
from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True, locale="es") as sb:
    url = "https://www.idealista.com/venta-viviendas/barcelona-provincia/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.solve_captcha()
    sb.sleep(2)
    endpoint_url = sb.cdp.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        page.click("button#didomi-notice-agree-button")
        page.wait_for_timeout(1000)
        print("*** " + page.locator("h1").inner_text())
        items = page.locator("div.item-info-container")
        for i in range(items.count()):
            item = items.nth(i)
            print(item.locator("a.item-link").text_content().strip())
            print(item.locator("span.item-price").text_content().strip())
            item_text = items.nth(i)
