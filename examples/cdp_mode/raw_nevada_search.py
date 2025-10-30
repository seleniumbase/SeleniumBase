"""Business Entity Search / Bypasses hCaptcha."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.nvsilverflume.gov/home"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.click('a[href="/redirectToCenuity/be"]')
    sb.sleep(3.6)
    sb.assert_element('label:contains("Business Search")')
    sb.click('input#BusinessSearch_Index_rdContains')
    sb.sleep(0.6)
    name_field = 'input[data-automation-id*="EntityName"]'
    search = "Laser Tag"
    sb.press_keys(name_field, search + "\n")
    sb.sleep(6.5)
    print('*** Business Search for "%s":' % search)
    businesses = sb.select_all("td a[onclick]")
    for business in businesses:
        print(business.text)
