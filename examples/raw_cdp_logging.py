"""NOTE: This uses plain UC Mode, which was replaced by UC + CDP Mode.
PyAutoGUI is installed automatically for uc_gui methods if not already."""
from rich.pretty import pprint
from seleniumbase import Driver

driver = Driver(uc=True, log_cdp=True)
try:
    url = "seleniumbase.io/apps/turnstile"
    driver.uc_open_with_reconnect(url, 2)
    driver.uc_gui_handle_captcha()
    driver.sleep(2)
    pprint(driver.get_log("performance"))
finally:
    driver.quit()
