from seleniumbase import sb_cdp

url = "https://www.nike.com/"
sb = sb_cdp.Chrome(url)
sb.click('div[data-testid="user-tools-container"]')
sb.sleep(1)
search = "Pegasus"
sb.press_keys('input[type="search"]', search)
sb.sleep(4)
elements = sb.select_all('ul[data-testid*="products"] figure .details')
if elements:
    print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
sb.driver.stop()
