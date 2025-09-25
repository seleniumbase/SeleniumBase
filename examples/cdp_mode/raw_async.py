import asyncio
import time
from contextlib import suppress
from seleniumbase import sb_cdp
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
    time.sleep(1)
    element = await page.select("h1")
    assert element.text == "Welcome!"
    driver.stop()

if __name__ == "__main__":
    # Call an async function with awaited methods
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

    # Call everything without using async / await
    driver = cdp_driver.start_sync()
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
    time.sleep(2)
    print(loop.run_until_complete(page.evaluate("document.title")))
    time.sleep(1)
    driver.stop()

    # Call CDP methods via the simplified SB CDP API
    sb = sb_cdp.Chrome("https://www.priceline.com/")
    sb.sleep(2.5)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(3.5)
    sb.remove_elements("msm-cookie-banner")
    sb.sleep(1.5)
    location = "Amsterdam"
    where_to = 'div[data-automation*="experiences"] input'
    button = 'button[data-automation*="experiences-search"]'
    sb.wait_for_text("Where to?")
    sb.gui_click_element(where_to)
    sb.press_keys(where_to, location)
    sb.sleep(1)
    sb.gui_click_element(button)
    sb.sleep(3)
    print(sb.get_title())
    print("************")
    cards = sb.select_all('span[data-automation*="product-list-card"]')
    for card in cards:
        print("* %s" % card.text)
    sb.driver.stop()
