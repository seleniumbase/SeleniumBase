"""(Bypasses Friendly Captcha)"""
import asyncio
from seleniumbase import cdp_driver


async def main():
    url = "https://muse.jhu.edu/verify"
    driver = await cdp_driver.start_async(guest=True)
    page = await driver.get(url)
    await page.sleep(2.5)
    await page.solve_captcha()
    await page.sleep(4)
    await page.find('#search_input')
    await page.sleep(3)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
