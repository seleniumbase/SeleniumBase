import asyncio
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver

url = "https://www.nike.com/"
loop = asyncio.new_event_loop()
driver = cdp_driver.cdp_util.start_sync()
page = loop.run_until_complete(driver.get(url))
sb = sb_cdp.CDPMethods(loop, page, driver)

search = "Nike Fly Shoes"
sb.click('div[data-testid="user-tools-container"]')
sb.sleep(1)
sb.press_keys('input[type="search"]', search)
sb.sleep(4)

elements = sb.select_all('ul[data-testid*="products"] figure .details')
if elements:
    print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
