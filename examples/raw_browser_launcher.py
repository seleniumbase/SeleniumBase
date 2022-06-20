"""
This script can be run with pure "python". (pytest not needed).
"get_driver()" is from [seleniumbase/core/browser_launcher.py].
"""
from seleniumbase import get_driver
from seleniumbase import js_utils
from seleniumbase import page_actions

driver = get_driver("chrome", headless=False)
try:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element_visible(driver, "4", "id").click()
    page_actions.wait_for_element_visible(driver, "2", "id").click()
    page_actions.wait_for_text_visible(driver, "42", "output", "id")
    js_utils.highlight_with_js(driver, "#output", 6, "")
finally:
    driver.quit()
