from seleniumbase import Driver

driver = Driver(mobile=True)
try:
    driver.open("https://www.roblox.com/")
    driver.assert_element("#download-the-app-container")
    driver.assert_text("Roblox for Android")
    driver.highlight('span:contains("Roblox for Android")', loops=8)
    driver.highlight('span:contains("Continue in App")', loops=8)
finally:
    driver.quit()
