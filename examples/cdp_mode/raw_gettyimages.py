from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", pls="none") as sb:
    sb.activate_cdp_mode("https://www.gettyimages.com/")
    sb.cdp.click('label:contains("Editorial")')
    sb.cdp.press_keys("form input", "comic con 2024 sci fi panel\n")
    sb.sleep(3)
    items = sb.cdp.find_elements("figure picture img")
    for item in items:
        item.flash(color="44CC88")
        sb.sleep(0.08)
