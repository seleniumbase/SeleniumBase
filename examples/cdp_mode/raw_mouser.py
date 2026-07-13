from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.mouser.com/")
    search_box = 'input[name="keyword"]'
    sb.sleep(1.6)
    sb.solve_captcha()
    sb.sleep(1.8)
    sb.wait_for_element(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, "FLUKE-TC01B 25HZ")
    sb.sleep(1.2)
    sb.click('button[type="submit"]')
    sb.sleep(3.2)
    sb.wait_for_element("span#spnDescription")
    soup = sb.get_beautiful_soup()
    print(soup.select_one("h1").get_text(strip=True))
    print(soup.select_one("span#spnDescription").get_text(strip=True))
    print(soup.select_one("td.ext-price-col").get_text(strip=True))
