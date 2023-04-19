"""Can run with "python". (pytest not needed)."""
from seleniumbase import js_utils
from seleniumbase import page_actions
from seleniumbase import DriverContext

# Driver Context Manager - (By default, browser="chrome". Lots of options)
with DriverContext() as driver:
    driver.get("https://seleniumbase.github.io/")
    js_utils.highlight_with_js(driver, 'img[alt="SeleniumBase"]', loops=6)

with DriverContext(browser="chrome", incognito=True) as driver:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element(driver, "4", by="id").click()
    page_actions.wait_for_element(driver, "2", by="id").click()
    page_actions.wait_for_text(driver, "42", "output", by="id")
    js_utils.highlight_with_js(driver, "#output", loops=6)

with DriverContext() as driver:
    driver.get("https://seleniumbase.github.io/demo_page")
    js_utils.highlight_with_js(driver, "h2", loops=5)
    by_css = "css selector"
    driver.find_element(by_css, "#myTextInput").send_keys("Automation")
    driver.find_element(by_css, "#checkBox1").click()
    js_utils.highlight_with_js(driver, "img", loops=5)
