import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.goto("https://seleniumbase.io/simple/login")
        await page.fill("#username", "demo_user")
        await page.fill("#password", "secret_pass")
        await page.click("#log-in")
        await page.wait_for_selector("h1")
        await driver.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
