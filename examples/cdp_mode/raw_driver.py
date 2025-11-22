import atexit
from seleniumbase import Driver

driver = Driver(uc=True, guest=True)
atexit.register(driver.quit)
url = "www.planetminecraft.com/account"
driver.activate_cdp_mode(url)
driver.sleep(2)
driver.solve_captcha()
driver.wait_for_element_absent("input[disabled]")
driver.sleep(2)
