"""DriverContext() example. (Runs with "python")."""
from seleniumbase import DriverContext

with DriverContext() as driver:
    driver.open("seleniumbase.io/")
    driver.highlight('img[alt="SeleniumBase"]', loops=6)

with DriverContext(browser="chrome", incognito=True) as driver:
    driver.open("seleniumbase.io/apps/calculator")
    driver.click('[id="4"]')
    driver.click('[id="2"]')
    driver.assert_text("42", "#output")
    driver.highlight("#output", loops=6)

with DriverContext() as driver:
    driver.open("seleniumbase.io/demo_page")
    driver.highlight("h2")
    driver.type("#myTextInput", "Automation")
    driver.click("#checkBox1")
    driver.highlight("img", loops=6)
