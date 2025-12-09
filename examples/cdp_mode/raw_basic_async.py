import asyncio
from seleniumbase import cdp_driver
from seleniumbase import decorators


async def main():
    url = "seleniumbase.io/simple/login"
    driver = await cdp_driver.start_async()
    page = await driver.get(url, lang="en")
    print(await page.get_title())
    await page.type("#username", "demo_user")
    await page.type("#password", "secret_pass")
    await page.click("#log-in")
    print(await page.get_title())
    element = await page.select("h1")
    assert element.text == "Welcome!"
    top_nav = await page.select("div.topnav")
    links = await top_nav.query_selector_all_async("a")
    for nav_item in links:
        print(nav_item.text)
    driver.stop()

if __name__ == "__main__":
    # Call an async function with awaited methods
    loop = asyncio.new_event_loop()
    with decorators.print_runtime("raw_basic_async.py"):
        loop.run_until_complete(main())
