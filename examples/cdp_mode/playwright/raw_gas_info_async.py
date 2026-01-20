import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()
    tab = await driver.get("about:blank")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        url = (
            "https://www.gassaferegister.co.uk/gas-safety"
            "/gas-safety-certificates-records/building-regulations-certificate"
            "/order-replacement-building-regulations-certificate/"
        )
        await page.goto(url)
        await tab.sleep(0.6)
        await tab.solve_captcha()
        await page.wait_for_selector("#SearchTerm")
        await tab.sleep(1.4)
        allow_cookies = 'button:contains("Allow all cookies")'
        await tab.click_if_visible(allow_cookies, timeout=2)
        await tab.sleep(1)
        await page.fill("#SearchTerm", "Hydrogen")
        await page.click("button.search-button")
        await tab.sleep(3)
        results = await tab.query_selector_all("div.search-result")
        for result in results:
            print(result.text.replace(" " * 12, " ").strip() + "\n")
        await tab.scroll_down(50)
        await tab.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
