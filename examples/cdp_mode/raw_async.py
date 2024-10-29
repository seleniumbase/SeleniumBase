import asyncio
import time
from contextlib import suppress
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


async def main():
    driver = await cdp_driver.cdp_util.start_async()
    page = await driver.get("about:blank")
    await page.set_locale("en")
    await page.get("https://www.priceline.com/")
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
    page = loop.run_until_complete(driver.get("about:blank"))
    loop.run_until_complete(page.set_locale("en"))
    loop.run_until_complete(page.get("https://www.pokemon.com/us"))
    time.sleep(3)
    print(loop.run_until_complete(page.evaluate("document.title")))
    with suppress(Exception):
        selector = "button#onetrust-reject-all-handler"
        element = loop.run_until_complete(page.select(selector, timeout=1))
        loop.run_until_complete(element.click_async())
        time.sleep(1)
    element = loop.run_until_complete(page.select("span.icon_pokeball"))
    loop.run_until_complete(element.click_async())
    time.sleep(1.5)
    print(loop.run_until_complete(page.evaluate("document.title")))
    time.sleep(1)

    # Call CDP methods via the simplified CDP API
    page = loop.run_until_complete(driver.get("about:blank"))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.set_locale("en")
    sb.open("https://www.priceline.com/")
    sb.sleep(3)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(2.5)
    sb.remove_elements("msm-cookie-banner")
    sb.sleep(1.5)
    location = "Amsterdam"
    sb.press_keys('input[data-test-id*="search"]', location)
    sb.sleep(1)
    sb.click('input[data-test-id*="search"]')
    sb.sleep(2)
    sb.click('span[data-test-id*="autocomplete"]')
    sb.sleep(5)
    print(sb.get_title())
