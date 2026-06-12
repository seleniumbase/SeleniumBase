from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.nike.com/")
sb.sleep(1.2)
sb.click('[data-testid="user-tools-container"] search')
sb.sleep(1)
search = "Pegasus"
sb.press_keys('input[type="search"]', search)
sb.sleep(4)
details = 'ul[data-testid*="products"] figure .details'
elements = sb.select_all(details)
if elements:
    print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
sb.quit()
