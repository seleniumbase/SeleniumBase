"""Example of using CDP Mode with WebDriver"""
from contextlib import suppress
from seleniumbase import SB


with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.priceline.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
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
