import os
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


@pytest.mark.offline  # Can be run with: "pytest -m offline"
class OfflineTests(BaseCase):
    def test_extended_driver(self):
        # Load a local html file into the web browser
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path, "demo_page.html")
        self.load_html_file(file_path)

        # Get the raw driver
        driver = self.driver

        # Assert that an element is visible on the page
        driver.assert_element("tbody#tbodyId")

        # Assert that a text substring appears in an element
        driver.assert_text("Demo Page", "h1")

        # Type text into various text fields and then assert
        driver.type("#myTextInput", "This is Automated")
        driver.type("textarea.area1", "Testing Time!\n")
        driver.type('[name="preText2"]', "Typing Text!")
        driver.assert_text("This is Automated", "#myTextInput")
        driver.assert_text("Testing Time!\n", "textarea.area1")
        driver.assert_text("Typing Text!", '[name="preText2"]')

        # Hover & click a dropdown element and assert results
        driver.assert_text("Automation Practice", "h3")
        driver.js_click("#dropOption2")
        driver.assert_text("Link Two Selected", "h3")

        # Click a button and then verify the expected results
        driver.assert_text("This Text is Green", "#pText")
        driver.click('button:contains("Click Me")')
        driver.assert_text("This Text is Purple", "#pText")

        # Assert that the given SVG is visible on the page
        driver.assert_element('svg[name="svgName"]')

        # Assert an element located inside an iframe
        self.assert_false(driver.is_element_visible("img"))
        driver.switch_to.frame("myFrame1")
        self.assert_true(driver.is_element_visible("img"))
        driver.switch_to.default_content()

        # Assert text located inside an iframe
        self.assert_false(driver.is_text_visible("iFrame Text"))
        driver.switch_to.frame("myFrame2")
        self.assert_true(driver.is_text_visible("iFrame Text"))
        driver.switch_to.default_content()

        # Assert exact text
        driver.assert_exact_text("Demo Page", "h1")

        # Highlight a page element (Also asserts visibility)
        driver.highlight("h2")
