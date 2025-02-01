from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url1 = "https://seleniumbase.io/demo_page"
    sb.activate_cdp_mode(url1)
    driver1 = sb.driver
    url2 = "https://seleniumbase.io/coffee/"
    driver2 = sb.get_new_driver(undetectable=True)
    sb.activate_cdp_mode(url2)
    print(driver1.get_current_url())
    print(driver2.get_current_url())
    sb.switch_to_default_driver()
    sb.assert_url_contains("demo_page")
    print(sb.get_current_url())
    sb.switch_to_driver(driver2)
    sb.assert_url_contains("coffee")
    print(sb.get_current_url())
