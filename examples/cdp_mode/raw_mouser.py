from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.mouser.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(5)
    sb.press_keys('input[name="keyword"]', "FLUKE-TC01B 25HZ")
    sb.click('button[type="submit"]')
    sb.sleep(2)
    print(sb.get_text("h1"))
    print(sb.get_text("span#spnDescription"))
    print(sb.get_text("td.ext-price-col"))
    sb.highlight("h1")
    sb.highlight("span#spnDescription")
    sb.highlight("td.ext-price-col")
