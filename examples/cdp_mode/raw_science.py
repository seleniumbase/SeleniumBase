from seleniumbase import SB

with SB(uc=True, incognito=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://earth.esa.int/eogateway/search")
    sb.sleep(1)
    sb.click_if_visible('button:contains("Accept cookies")', timeout=3)
    for i in range(20):
        sb.scroll_to_bottom()
        sb.click_if_visible('button:contains("READ MORE")')
    sb.sleep(1)
    elements = sb.find_elements("h4 a span")
    for element in elements:
        print(element.text)
    print("*** Total entries: %s" % len(elements))
