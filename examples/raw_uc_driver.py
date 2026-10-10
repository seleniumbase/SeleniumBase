"""UC Mode Driver for evading bot-detection."""
from seleniumbase import Driver

driver = Driver(uc=True)
driver.get("https://browserscan.net/bot-detection")
driver.assert_element('strong:contains("Normal")')
driver.sleep(1)
driver.get("https://bot.sannysoft.com/")
driver.assert_element(".passed")
driver.assert_element_not_visible(".failed")
driver.sleep(1)
driver.quit()
