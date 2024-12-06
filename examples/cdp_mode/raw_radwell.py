from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", incognito=True) as sb:
    url = "https://www.radwell.com/en-US/Search/Advanced/"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.cdp.press_keys("form#basicsearch input", "821C-PM-111DA-142")
    sb.sleep(1)
    sb.cdp.click('[value="Search Icon"]')
    sb.sleep(3)
    sb.cdp.assert_text("MAC VALVES INC", "a.manufacturer-link")
    sb.cdp.highlight("a.manufacturer-link")
    sb.sleep(1)
