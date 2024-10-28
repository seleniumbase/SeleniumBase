"""Example of using CDP Mode without WebDriver"""
import asyncio
from contextlib import suppress
from seleniumbase import decorators
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


@decorators.print_runtime("CDP Priceline Example")
def main():
    url0 = "about:blank"  # Set Locale code from here first
    url1 = "https://www.priceline.com/"  # (The "real" URL)
    loop = asyncio.new_event_loop()
    driver = cdp_driver.cdp_util.start_sync()
    page = loop.run_until_complete(driver.get(url0))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.set_locale("en")  # This test expects English locale
    sb.open(url1)
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
    header = sb.get_text('h2[data-testid*="RelatedVenues"]')
    print("*** %s: ***" % header)
    cards = sb.select_all("div.venue-card__body")
    for card in cards:
        with suppress(Exception):
            venue = card.text.split("\n")[0].strip()
            rating = card.text.split("\n")[1].strip()
            reviews = card.text.split("\n")[2].strip()[1:-1]
            print("* %s: %s from %s reviews." % (venue, rating, reviews))


if __name__ == "__main__":
    main()
