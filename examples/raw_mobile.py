from seleniumbase import Driver

driver = Driver(mobile=True)
try:
    driver.open("https://www.skype.com/en/get-skype/")
    driver.assert_element('[aria-label="Microsoft"]')
    driver.assert_text("Download Skype", "h1")
    driver.highlight("div.appBannerContent")
    driver.highlight("h1")
    driver.assert_text("Skype for Mobile", "h2")
    driver.highlight("h2")
    driver.highlight("#get-skype-0")
    driver.highlight_click("span[data-dropdown-icon]")
    driver.highlight("#get-skype-0_android-download")
    driver.highlight('[data-bi-id*="ios"]')
finally:
    driver.quit()
