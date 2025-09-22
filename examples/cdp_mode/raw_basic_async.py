import asyncio
from seleniumbase import cdp_driver


async def main():
    url = "seleniumbase.io/simple/login"
    driver = await cdp_driver.start_async(incognito=True)
    page = await driver.get(url)
    print(await page.evaluate("document.title"))
    element = await page.select("#username")
    await element.send_keys_async("demo_user")
    element = await page.select("#password")
    await element.send_keys_async("secret_pass")
    element = await page.select("#log-in")
    await element.click_async()
    print(await page.evaluate("document.title"))
    element = await page.select("h1")
    assert element.text == "Welcome!"
    top_nav = await page.select("div.topnav")
    links = await top_nav.query_selector_all_async("a")
    for nav_item in links:
        print(nav_item.text)

if __name__ == "__main__":
    # Call an async function with awaited methods
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
