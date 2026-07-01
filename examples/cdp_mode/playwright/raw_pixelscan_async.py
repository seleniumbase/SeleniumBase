import asyncio
import time
from playwright.async_api import async_playwright
from playwright.async_api import expect
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        await page.goto("https://pixelscan.net/fingerprint-check")
        time.sleep(4)
        await expect(
            page.locator("pxlscn-bot-detection")
        ).to_contain_text("No automated behavior", timeout=4000)
        await page.wait_for_selector("span.status-success", timeout=4000)
        await expect(
            page.locator("pxlscn-fingerprint-masking")
        ).to_contain_text("No masking detected", timeout=4000)
        time.sleep(2)
        print("Bot Not Detected")


if __name__ == "__main__":
    asyncio.run(main())
