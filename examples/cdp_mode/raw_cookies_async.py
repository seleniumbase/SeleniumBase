"""A script that loads cookies to bypass login."""
import asyncio
import time
from seleniumbase import cdp_driver


# Log in to Swag Labs and save cookies
async def get_login_cookies():
    url = "https://www.saucedemo.com"
    driver = await cdp_driver.start_async(incognito=True)
    page = await driver.get(url)
    element = await page.select("#user-name")
    await element.send_keys_async("standard_user")
    element = await page.select("#password")
    await element.send_keys_async("secret_sauce")
    element = await page.select('input[type="submit"]')
    await element.click_async()
    cookies = await driver.cookies.get_all()
    driver.stop()
    return cookies


# Load previously saved cookies to bypass login
async def login_with_cookies(cookies):
    url_1 = "https://www.saucedemo.com"
    url_2 = "https://www.saucedemo.com/inventory.html"
    driver = await cdp_driver.start_async()
    page = await driver.get(url_1)
    await driver.cookies.set_all(cookies)
    await driver.get(url_2)
    await page.select("div.inventory_list")
    time.sleep(2)
    driver.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    cookies = loop.run_until_complete(get_login_cookies())
    loop.run_until_complete(login_with_cookies(cookies))
