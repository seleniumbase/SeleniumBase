import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver


async def main():
    driver = await cdp_driver.start_async(locale="en", agent="headless")
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.goto("https://gitlab.com/users/sign_in")
        await driver.sleep(3)
        await driver.solve_captcha()
        await driver.sleep(1)
        await page.locator('label[for="user_login"]').click()
        await page.wait_for_selector('[data-testid="sign-in-button"]')
        await page.locator("#user_login").fill("Username")
        await driver.sleep(2)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
