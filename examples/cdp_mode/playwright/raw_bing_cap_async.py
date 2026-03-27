import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async(locale="en")
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        await page.goto("https://www.bing.com/turing/captcha/challenge")
        await page.wait_for_timeout(2000)
        await driver.solve_captcha()
        await page.wait_for_timeout(2000)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
