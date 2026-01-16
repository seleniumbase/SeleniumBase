from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    url = "https://www.radwell.com/en-US/Search/Advanced/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.press_keys("form#basicsearch input", "821C-PM-111DA-142")
    sb.click('[value="Search Icon"]')
    sb.sleep(2)
    if not sb.is_element_visible("a.manufacturer-link"):
        sb.solve_captcha()
        sb.sleep(0.5)
    sb.assert_text("MAC VALVES INC", "a.manufacturer-link")
    sb.highlight("a.manufacturer-link")
    description = sb.get_text("div.product-information")
    description = description.replace("                ", "")
    description = description.replace("\n             \n", "\n")
    print(description)
    sb.sleep(1)
