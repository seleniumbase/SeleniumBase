from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class DemoSiteTests(BaseCase):
    def test_demo_site(self):
        # Open a web page in the active browser window
        self.open("https://seleniumbase.io/demo_page")

        # Assert the title of the current web page
        self.assert_title("Web Testing Page")

        # Assert that an element is visible on the page
        self.assert_element("tbody#tbodyId")

        # Assert that a text substring appears in an element
        self.assert_text("Demo Page", "h1")

        # Type text into various text fields and then assert
        self.type("#myTextInput", "This is Automated")
        self.type("textarea.area1", "Testing Time!\n")
        self.type('[name="preText2"]', "Typing Text!")
        self.assert_text("This is Automated", "#myTextInput")
        self.assert_text("Testing Time!\n", "textarea.area1")
        self.assert_text("Typing Text!", '[name="preText2"]')

        # Hover & click a dropdown element and assert results
        self.assert_text("Automation Practice", "h3")
        try:
            self.hover_and_click("#myDropdown", "#dropOption2", timeout=1)
        except Exception:
            # Someone probably moved the mouse while the test ran
            self.hover_and_js_click("#myDropdown", "#dropOption2")
        self.assert_text("Link Two Selected", "h3")

        # Click a button and then verify the expected results
        self.assert_text("This Text is Green", "#pText")
        self.click('button:contains("Click Me")')
        self.assert_text("This Text is Purple", "#pText")

        # Assert that the given SVG is visible on the page
        self.assert_element('svg[name="svgName"]')

        # Verify that a slider control updates a progress bar
        self.assert_element('progress[value="50"]')
        self.set_value("input#mySlider", "100")
        self.assert_element('progress[value="100"]')

        # Verify that a "select" option updates a meter bar
        self.assert_element('meter[value="0.25"]')
        self.select_option_by_text("#mySelect", "Set to 75%")
        self.assert_element('meter[value="0.75"]')

        # Assert an element located inside an iframe
        self.assert_false(self.is_element_visible("img"))
        self.switch_to_frame("#myFrame1")
        self.assert_true(self.is_element_visible("img"))
        self.switch_to_default_content()

        # Assert text located inside an iframe
        self.assert_false(self.is_text_visible("iFrame Text"))
        self.switch_to_frame("#myFrame2")
        self.assert_true(self.is_text_visible("iFrame Text"))
        self.switch_to_default_content()

        # Verify that clicking a radio button selects it
        self.assert_false(self.is_selected("#radioButton2"))
        self.click("#radioButton2")
        self.assert_true(self.is_selected("#radioButton2"))

        # Verify that clicking a checkbox makes it selected
        self.assert_element_not_visible("img#logo")
        self.assert_false(self.is_selected("#checkBox1"))
        self.click("#checkBox1")
        self.assert_true(self.is_selected("#checkBox1"))
        self.assert_element("img#logo")

        # Verify clicking on multiple elements with one call
        self.assert_false(self.is_selected("#checkBox2"))
        self.assert_false(self.is_selected("#checkBox3"))
        self.assert_false(self.is_selected("#checkBox4"))
        self.click_visible_elements("input.checkBoxClassB")
        self.assert_true(self.is_selected("#checkBox2"))
        self.assert_true(self.is_selected("#checkBox3"))
        self.assert_true(self.is_selected("#checkBox4"))

        # Verify that clicking an iframe checkbox selects it
        self.assert_false(self.is_element_visible(".fBox"))
        self.switch_to_frame("#myFrame3")
        self.assert_true(self.is_element_visible(".fBox"))
        self.assert_false(self.is_selected(".fBox"))
        self.click(".fBox")
        self.assert_true(self.is_selected(".fBox"))
        self.switch_to_default_content()

        # Verify Drag and Drop
        self.assert_element_not_visible("div#drop2 img#logo")
        self.drag_and_drop("img#logo", "div#drop2")
        self.assert_element("div#drop2 img#logo")

        # Assert link text
        self.assert_link_text("seleniumbase.com")
        self.assert_link_text("SeleniumBase on GitHub")
        self.assert_link_text("seleniumbase.io")

        # Click link text
        self.click_link("SeleniumBase Demo Page")

        # Assert exact text
        self.assert_exact_text("Demo Page", "h1")

        # Highlight a page element (Also asserts visibility)
        self.highlight("h2")

        # Actions with Demo Mode enabled
        if self.headed:
            self.activate_demo_mode()
        self.type("input", "Have a Nice Day!")
        self.assert_text("SeleniumBase", "h2")
