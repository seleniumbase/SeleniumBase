from seleniumbase import Driver

driver = Driver(mobile=True)
try:
    driver.open("https://www.roblox.com/")
    driver.assert_element("#download-the-app-container")
    driver.assert_text("Roblox for Android", "p.roblox-for-platform")
    driver.assert_text("Continue in App", "a.primary-link")
    driver.highlight("p.roblox-for-platform", loops=8)
    driver.highlight("a.primary-link", loops=8)
finally:
    driver.quit()
