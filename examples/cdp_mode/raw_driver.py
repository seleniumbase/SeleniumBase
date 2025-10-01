import atexit
from seleniumbase import Driver

driver = Driver(uc=True)
atexit.register(driver.quit)
url = "www.planetminecraft.com/account"
driver.uc_activate_cdp_mode(url)
driver.sleep(1)
driver.uc_gui_click_captcha()
driver.wait_for_element_absent("input[disabled]")
driver.sleep(2)
