"""Example of using various CDP Mode commands."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://seleniumbase.io/demo_page")

    # Assert various things
    sb.assert_title("Web Testing Page")
    sb.assert_element("tbody#tbodyId")
    sb.assert_text("Demo Page", "h1")

    # Type text into various text fields and then assert
    sb.type("#myTextInput", "This is Automated")
    sb.type("textarea.area1", "Testing Time!\n")
    sb.type('[name="preText2"]', "Typing Text!")
    sb.assert_text("This is Automated", "#myTextInput")
    sb.assert_text("Testing Time!\n", "textarea.area1")
    sb.assert_text("Typing Text!", '[name="preText2"]')

    # Hover & click a dropdown element and assert results
    sb.assert_text("Automation Practice", "h3")
    sb.hover_and_click("#myDropdown", "#dropOption2")
    sb.assert_text("Link Two Selected", "h3")

    # Click a button and then verify the expected results
    sb.assert_text("This Text is Green", "#pText")
    sb.click('button:contains("Click Me")')
    sb.assert_text("This Text is Purple", "#pText")

    # Verify that a slider control updates a progress bar
    sb.assert_element('progress[value="50"]')
    sb.set_value("input#mySlider", "100")
    sb.assert_element('progress[value="100"]')

    # Verify that a "select" option updates a meter bar
    sb.assert_element('meter[value="0.25"]')
    sb.select_option_by_text("#mySelect", "Set to 75%")
    sb.assert_element('meter[value="0.75"]')

    # Verify that clicking a radio button selects it
    sb.assert_false(sb.is_selected("#radioButton2"))
    sb.click("#radioButton2")
    sb.assert_true(sb.is_selected("#radioButton2"))

    # Verify that clicking a checkbox makes it selected
    sb.assert_element_not_visible("img#logo")
    sb.assert_false(sb.is_selected("#checkBox1"))
    sb.click("#checkBox1")
    sb.assert_true(sb.is_selected("#checkBox1"))
    sb.assert_element("img#logo")

    # Verify clicking on multiple elements with one call
    sb.assert_false(sb.is_selected("#checkBox2"))
    sb.assert_false(sb.is_selected("#checkBox3"))
    sb.assert_false(sb.is_selected("#checkBox4"))
    sb.click_visible_elements("input.checkBoxClassB")
    sb.assert_true(sb.is_selected("#checkBox2"))
    sb.assert_true(sb.is_selected("#checkBox3"))
    sb.assert_true(sb.is_selected("#checkBox4"))

    # Verify Drag and Drop
    sb.assert_element_not_visible("div#drop2 img#logo")
    sb.gui_drag_and_drop("img#logo", "div#drop2")
    sb.assert_element("div#drop2 img#logo")

    # Click inside an iframe and test highlighting
    sb.flash("iframe#myFrame3")
    sb.sleep(1)
    sb.nested_click("iframe#myFrame3", ".fBox")
    sb.sleep(0.5)
    sb.highlight("iframe#myFrame3")
