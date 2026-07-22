"""An example that bypasses the DataDome Slider CAPTCHA.
(PyAutoGUI is installed at runtime if not yet installed.)"""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
sb.goto("https://www.immoscout24.ch/en/real-estate/rent")
sb.sleep(1.6)
sb.solve_captcha()
sb.sleep(2.5)
sb.click_if_visible("#onetrust-accept-btn-handler", timeout=3)
sb.sleep(0.5)
sb.click('[data-cy="Locations_searchFieldOpener"]')
sb.sleep(0.6)
sb.press_keys('[data-cy="Locations_searchField"]', "Bern")
sb.sleep(0.6)
sb.click_if_visible('b:contains("Bern")', timeout=2)
sb.sleep(2.1)
sb.click('button[data-cy="SearchBar_button"]')
sb.sleep(3.5)
print("*** " + sb.get_text("h1"))
items = sb.find_elements('[data-test="result-list-item"]')
for item in items:
    item.flash(color="44CC88")
    print(item.query_selector('[class*="mainTitle"]').text)
    print(item.query_selector("address").text)
