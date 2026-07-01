"""UC Mode Driver for evading bot-detection."""
from seleniumbase import Driver

driver = Driver(uc=True)
driver.get("https://browserscan.net/bot-detection")
driver.assert_element('strong:contains("Normal")')
driver.sleep(1)
driver.get("https://bot.sannysoft.com/")
driver.assert_element("#user-agent-result.passed")
driver.assert_element("#webdriver-result.passed")
driver.assert_element("#advanced-webdriver-result.passed")
driver.assert_element("#permissions-result.passed")
driver.assert_element("#plugins-length-result.passed")
driver.assert_element("#plugins-type-result.passed")
driver.sleep(1)
driver.quit()
