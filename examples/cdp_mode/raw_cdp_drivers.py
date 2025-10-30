# An example of switching between multiple drivers
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url1 = "https://seleniumbase.io/antibot/login"
    sb.activate_cdp_mode(url1)
    url2 = "https://seleniumbase.io/hobbit/login"
    driver2 = sb.get_new_driver(undetectable=True)
    sb.activate_cdp_mode(url2)
    sb.sleep(1)
    sb.switch_to_default_driver()
    sb.assert_url_contains("antibot")
    print(sb.get_current_url())
    sb.type("input#username", "demo_user")
    sb.type("input#password", "secret_pass")
    sb.click("button")
    sb.sleep(1)
    sb.click("a#log-in")
    sb.assert_text("Welcome!", "h1")
    sb.sleep(2)
    sb.switch_to_driver(driver2)
    sb.assert_url_contains("hobbit")
    print(sb.get_current_url())
    sb.click("button")
    sb.assert_text("Welcome to Middle Earth!")
    sb.click("img")
    sb.sleep(3)
