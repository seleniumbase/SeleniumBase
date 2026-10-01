"""Business Entity Search"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.nvsilverflume.gov/home")
    sb.sleep(3.6)
    sb.click('span:contains("Search Business Entities")')
    sb.sleep(3.6)
    sb.assert_element('strong:contains("Search for a Business")')
    sb.sleep(1)
    sb.click('[data-type="select-one"]')
    sb.sleep(0.5)
    sb.click('label:contains("Search Type")')
    sb.sleep(0.5)
    sb.click('div[data-value="CONTAINS"]')
    sb.sleep(0.5)
    name_field = 'input[name="data[entityName]"]'
    search = "Laser Tag"
    sb.press_keys(name_field, search)
    sb.sleep(1)
    sb.click('button:contains("Search")')
    sb.sleep(2)
    print('*** Business Search for "%s":' % search)
    businesses = sb.select_all("tr.k-master-row")
    for business in businesses:
        print(business.text)
