from rich.pretty import pprint
from seleniumbase import Driver

driver = Driver(uc=True, log_cdp=True)
try:
    driver.get("https://seleniumbase.io/apps/invisible_recaptcha")
    driver.sleep(3)
    pprint(driver.get_log("performance"))
finally:
    driver.quit()
