"""Driver() test. Runs with "python". (pytest not needed)."""
from seleniumbase import Driver

driver = Driver(browser="chrome", headless=False)
try:
    driver.get("https://seleniumbase.io/apps/calculator")
    driver.click('[id="4"]')
    driver.click('[id="2"]')
    driver.assert_text("42", "#output")
    driver.highlight("#output", loops=6)
finally:
    driver.quit()

driver = Driver()
try:
    driver.get("https://seleniumbase.github.io/demo_page")
    driver.highlight("h2")
    driver.type("#myTextInput", "Automation")
    driver.click("#checkBox1")
    driver.highlight("img", loops=6)
finally:
    driver.quit()
