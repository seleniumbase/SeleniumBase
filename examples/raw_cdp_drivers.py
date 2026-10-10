from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.goto("https://browserscan.net/bot-detection")
    driver1 = sb.driver
    driver2 = sb.get_new_driver(uc=True)
    sb.goto("https://bot.sannysoft.com/")
    print(driver1.get_current_url())
    print(driver2.get_current_url())
    sb.switch_to_default_driver()
    sb.assert_element('strong:contains("Normal")')
    print(sb.get_current_url())
    sb.switch_to_driver(driver2)
    sb.assert_element(".passed")
    sb.assert_element_not_visible(".failed")
    print(sb.get_current_url())
