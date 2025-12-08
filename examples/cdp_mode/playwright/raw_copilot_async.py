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
        await page.goto("https://copilot.microsoft.com")
        await page.wait_for_selector("textarea#userInput")
        await driver.sleep(1)
        query = "Playwright Python connect_over_cdp() sync example"
        await page.fill("textarea#userInput", query)
        await page.click('button[data-testid="submit-button"]')
        await driver.sleep(3)
        await driver.solve_captcha()
        await page.wait_for_selector('button[data-testid*="-thumbs-up"]')
        await driver.sleep(4)
        await page.click('button[data-testid*="scroll-to-bottom"]')
        await driver.sleep(3)
        chat_results = '[data-testid="highlighted-chats"]'
        result = await page.locator(chat_results).inner_text()
        print(result.replace("\n\n", " \n"))


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
