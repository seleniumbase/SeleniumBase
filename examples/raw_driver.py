from seleniumbase import js_utils
from seleniumbase import page_actions
from seleniumbase import Driver

with Driver() as driver:
    driver.get("https://google.com/ncr")
    js_utils.highlight_with_js(driver, 'img[alt="Google"]', 6, "")

with Driver() as driver:  # By default, browser="chrome"
    driver.get("https://seleniumbase.github.io/demo_page")
    js_utils.highlight_with_js(driver, "h2", 5, "")
    CSS = "css selector"
    driver.find_element(CSS, "#myTextInput").send_keys("Automation")
    driver.find_element(CSS, "#checkBox1").click()
    js_utils.highlight_with_js(driver, "img", 5, "")

with Driver(browser="chrome", incognito=True) as driver:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element_visible(driver, "4", "id").click()
    page_actions.wait_for_element_visible(driver, "2", "id").click()
    page_actions.wait_for_text_visible(driver, "42", "output", "id")
    js_utils.highlight_with_js(driver, "#output", 6, "")
