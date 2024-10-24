import asyncio
import time
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


async def main():
    driver = await cdp_driver.cdp_util.start_async()
    page = await driver.get("https://www.priceline.com/")
    time.sleep(3)
    print(await page.evaluate("document.title"))
    element = await page.select('[data-testid*="endLocation"]')
    await element.click_async()
    time.sleep(1)
    await element.send_keys_async("Boston")
    time.sleep(2)

if __name__ == "__main__":
    # Call an async function with awaited methods
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

    # Call everything without using async / await
    driver = cdp_driver.cdp_util.start_sync()
    page = loop.run_until_complete(driver.get("https://www.pokemon.com/us"))
    time.sleep(3)
    print(loop.run_until_complete(page.evaluate("document.title")))
    element = loop.run_until_complete(page.select("span.icon_pokeball"))
    loop.run_until_complete(element.click_async())
    time.sleep(1)
    print(loop.run_until_complete(page.evaluate("document.title")))
    time.sleep(1)

    # Call CDP methods via the simplified CDP API
    page = loop.run_until_complete(driver.get("https://www.priceline.com/"))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.sleep(3)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(2)
    sb.remove_element("msm-cookie-banner")
    sb.sleep(1)
    sb.press_keys('input[data-test-id*="search"]', "Amsterdam")
    sb.sleep(2)
    sb.click('span[data-test-id*="autocomplete"]')
    sb.sleep(5)
    print(sb.get_title())
