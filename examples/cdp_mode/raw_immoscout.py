"""An example that bypasses the DataDome Slider CAPTCHA.
(PyAutoGUI is installed at runtime if not yet installed.)"""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.immoscout24.ch/en/real-estate/rent")
    sb.sleep(1.5)
    sb.solve_captcha()
    sb.sleep(2.5)
    sb.click_if_visible("#onetrust-accept-btn-handler")
    sb.sleep(0.5)
    sb.click('[data-cy="Locations_searchFieldOpener"]')
    sb.sleep(0.5)
    sb.press_keys('[data-cy="Locations_searchField"]', "Bern")
    sb.sleep(0.6)
    sb.click('b:contains("Bern")')
    sb.sleep(2.1)
    sb.click('button[data-cy="SearchBar_button"]')
    sb.sleep(3.5)
    print("*** " + sb.get_text("h1"))
    items = sb.find_elements('[data-test="result-list-item"]')
    for item in items:
        item.flash(color="44CC88")
        print(item.querySelector('[class*="mainTitle"]').text)
        print(item.querySelector("address").text)
