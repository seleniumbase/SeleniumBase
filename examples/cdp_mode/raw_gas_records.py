"""(Bypasses the Imperva/Incapsula hCaptcha)"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = (
        "https://www.gassaferegister.co.uk/gas-safety"
        "/gas-safety-certificates-records/building-regulations-certificate"
        "/order-replacement-building-regulations-certificate/"
    )
    sb.activate_cdp_mode(url)
    sb.sleep(0.6)
    sb.solve_captcha()
    sb.sleep(1)
    sb.wait_for_element("#SearchTerm", timeout=5)
    sb.sleep(2)
    allow_cookies = 'button:contains("Allow all cookies")'
    sb.click_if_visible(allow_cookies, timeout=2)
    sb.sleep(1.2)
    sb.press_keys("#SearchTerm", "Hydrogen")
    sb.sleep(0.5)
    sb.click("button.search-button")
    sb.sleep(3)
    results = sb.find_elements("div.search-result")
    for result in results:
        print(result.text.replace(" " * 12, " ").strip())
        print()
    sb.scroll_to_bottom()
    sb.sleep(1)
