"""This script can be run with pure "python". (pytest not needed)."""
from seleniumbase import js_utils
from seleniumbase import page_actions
from seleniumbase import Driver

# Python Context Manager
with Driver() as driver:  # By default, browser="chrome"
    driver.get("https://google.com/ncr")
    js_utils.highlight_with_js(driver, 'img[alt="Google"]', 6, "")

with Driver() as driver:  # Also accepts command-line options
    driver.get("https://seleniumbase.github.io/demo_page")
    js_utils.highlight_with_js(driver, "h2", 5, "")
    by_css = "css selector"
    driver.find_element(by_css, "#myTextInput").send_keys("Automation")
    driver.find_element(by_css, "#checkBox1").click()
    js_utils.highlight_with_js(driver, "img", 5, "")

# Python Context Manager (with options given)
with Driver(browser="chrome", incognito=True) as driver:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element(driver, "4", "id").click()
    page_actions.wait_for_element(driver, "2", "id").click()
    page_actions.wait_for_text(driver, "42", "output", "id")
    js_utils.highlight_with_js(driver, "#output", 6, "")
