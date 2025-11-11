"""Simple web-scraping example in CDP Mode"""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://architectureofcities.com/roman-theaters"
    sb.activate_cdp_mode(url)
    sb.sleep(0.5)
    sb.click_if_visible("#cn-close-notice")
    sb.click_if_visible('[aria-label="Reject All"]')
    sb.click_if_visible('span:contains("Continue")')
    sb.sleep(1)
    print("*** " + sb.get_text("h1") + " ***")
    for item in sb.find_elements("h3"):
        if item.text and "." in item.text:
            item.flash(color="44CC88")
            sb.scroll_down(34)
            print("* " + item.text.replace("  ", " "))
            sb.sleep(0.15)
    sb.sleep(1)
