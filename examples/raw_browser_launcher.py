"""
This script can be run with pure "python". (pytest not needed).
"get_driver()" is from [seleniumbase/core/browser_launcher.py].
"""
from seleniumbase import get_driver
from seleniumbase import js_utils
from seleniumbase import page_actions

success = False
try:
    driver = get_driver("chrome", headless=False)
    driver.get('data:text/html,<h1 class="top">Data URL</h2>')
    source = driver.page_source
    assert "Data URL" in source
    # An example of "is_element_visible()" from "page_actions"
    assert page_actions.is_element_visible(driver, "h1.top")
    # Extra fun with Javascript
    js_utils.highlight_with_js(driver, "h1.top", 8, "")
    success = True  # No errors
finally:
    driver.quit()
assert success
