from rich.pretty import pprint
from seleniumbase import Driver

driver = Driver(uc=True, log_cdp=True)
try:
    url = "seleniumbase.io/apps/turnstile"
    driver.uc_open_with_reconnect(url, 2)
    driver.switch_to_frame("iframe")
    driver.uc_click("span")
    driver.sleep(3)
    pprint(driver.get_log("performance"))
finally:
    driver.quit()
