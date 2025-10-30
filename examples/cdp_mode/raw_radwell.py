from seleniumbase import SB

with SB(uc=True, test=True, locale="en", incognito=True) as sb:
    url = "https://www.radwell.com/en-US/Search/Advanced/"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.press_keys("form#basicsearch input", "821C-PM-111DA-142")
    sb.sleep(1)
    sb.click('[value="Search Icon"]')
    sb.sleep(3)
    sb.assert_text("MAC VALVES INC", "a.manufacturer-link")
    sb.highlight("a.manufacturer-link")
    sb.sleep(1)
