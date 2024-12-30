"""Simple web-scraping example in CDP Mode"""
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://architectureofcities.com/roman-theaters"
    sb.activate_cdp_mode(url)
    sb.cdp.click_if_visible("#cn-close-notice")
    sb.sleep(1)
    print("*** " + sb.cdp.get_text("h1") + " ***")
    for item in sb.cdp.find_elements("h3"):
        if item.text and "." in item.text:
            item.flash(color="44CC88")
            sb.cdp.scroll_down(34)
            print("* " + item.text.replace("  ", " "))
            sb.sleep(0.15)
    sb.sleep(1)
