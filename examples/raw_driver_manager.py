"""Driver() manager example. (Runs with "python")."""
from seleniumbase import Driver

driver = Driver()
try:
    driver.open("seleniumbase.io/demo_page")
    driver.highlight("h2")
    driver.type("#myTextInput", "Automation")
    driver.click("#checkBox1")
    driver.highlight("img", loops=6)
finally:
    driver.quit()

driver = Driver(browser="chrome", headless=False)
try:
    driver.open("seleniumbase.io/apps/calculator")
    driver.click('[id="4"]')
    driver.click('[id="2"]')
    driver.assert_text("42", "#output")
    driver.highlight("#output", loops=6)
finally:
    driver.quit()
