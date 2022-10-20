"""This script can be run with pure "python". (pytest not needed)."""
from seleniumbase import Driver
from seleniumbase import js_utils
from seleniumbase import page_actions

# Example with options. (Also accepts command-line options.)
driver = Driver(browser="chrome", headless=False)
try:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element(driver, "4", "id").click()
    page_actions.wait_for_element(driver, "2", "id").click()
    page_actions.wait_for_text(driver, "42", "output", "id")
    js_utils.highlight_with_js(driver, "#output", 6, "")
finally:
    driver.quit()

# Example 2 using default args or command-line options
driver = Driver()
driver.get("https://seleniumbase.github.io/demo_page")
js_utils.highlight_with_js(driver, "h2", 5, "")
by_css = "css selector"
driver.find_element(by_css, "#myTextInput").send_keys("Automation")
driver.find_element(by_css, "#checkBox1").click()
js_utils.highlight_with_js(driver, "img", 5, "")
driver.quit()  # If the script fails early, the driver still quits
