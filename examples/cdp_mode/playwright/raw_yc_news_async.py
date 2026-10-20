import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        url = "https://hn.algolia.com/?query=seleniumbase"
        await page.goto(url)
        items = page.locator("div.Story_title > a")
        for i in range(await (items.count())):
            item_text = await (items.nth(i)).inner_text()
            print("* " + item_text)


if __name__ == "__main__":
    asyncio.run(main())
