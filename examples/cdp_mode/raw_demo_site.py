"""Example of using various CDP Mode commands"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/demo_page"
    sb.activate_cdp_mode(url)

    # Assert various things
    sb.cdp.assert_title("Web Testing Page")
    sb.cdp.assert_element("tbody#tbodyId")
    sb.cdp.assert_text("Demo Page", "h1")

    # Type text into various text fields and then assert
    sb.cdp.type("#myTextInput", "This is Automated")
    sb.cdp.type("textarea.area1", "Testing Time!\n")
    sb.cdp.type('[name="preText2"]', "Typing Text!")
    sb.cdp.assert_text("This is Automated", "#myTextInput")
    sb.cdp.assert_text("Testing Time!\n", "textarea.area1")
    sb.cdp.assert_text("Typing Text!", '[name="preText2"]')

    # Hover & click a dropdown element and assert results
    sb.cdp.assert_text("Automation Practice", "h3")
    sb.cdp.gui_hover_and_click("#myDropdown", "#dropOption2")
    sb.cdp.assert_text("Link Two Selected", "h3")

    # Click a button and then verify the expected results
    sb.cdp.assert_text("This Text is Green", "#pText")
    sb.cdp.click('button:contains("Click Me")')
    sb.cdp.assert_text("This Text is Purple", "#pText")

    # Verify that a slider control updates a progress bar
    sb.cdp.assert_element('progress[value="50"]')
    sb.cdp.set_value("input#mySlider", "100")
    sb.cdp.assert_element('progress[value="100"]')

    # Verify that a "select" option updates a meter bar
    sb.cdp.assert_element('meter[value="0.25"]')
    sb.cdp.select_option_by_text("#mySelect", "Set to 75%")
    sb.cdp.assert_element('meter[value="0.75"]')

    # Verify that clicking a radio button selects it
    sb.cdp.assert_false(sb.cdp.is_selected("#radioButton2"))
    sb.cdp.click("#radioButton2")
    sb.cdp.assert_true(sb.cdp.is_selected("#radioButton2"))

    # Verify that clicking a checkbox makes it selected
    sb.cdp.assert_element_not_visible("img#logo")
    sb.cdp.assert_false(sb.cdp.is_selected("#checkBox1"))
    sb.cdp.click("#checkBox1")
    sb.cdp.assert_true(sb.cdp.is_selected("#checkBox1"))
    sb.cdp.assert_element("img#logo")

    # Verify clicking on multiple elements with one call
    sb.cdp.assert_false(sb.cdp.is_selected("#checkBox2"))
    sb.cdp.assert_false(sb.cdp.is_selected("#checkBox3"))
    sb.cdp.assert_false(sb.cdp.is_selected("#checkBox4"))
    sb.cdp.click_visible_elements("input.checkBoxClassB")
    sb.cdp.assert_true(sb.cdp.is_selected("#checkBox2"))
    sb.cdp.assert_true(sb.cdp.is_selected("#checkBox3"))
    sb.cdp.assert_true(sb.cdp.is_selected("#checkBox4"))

    # Verify Drag and Drop
    sb.cdp.assert_element_not_visible("div#drop2 img#logo")
    sb.cdp.gui_drag_and_drop("img#logo", "div#drop2")
    sb.cdp.assert_element("div#drop2 img#logo")

    # Click inside an iframe and test highlighting
    sb.cdp.flash("iframe#myFrame3")
    sb.cdp.sleep(1)
    sb.cdp.nested_click("iframe#myFrame3", ".fBox")
    sb.cdp.sleep(0.5)
    sb.cdp.highlight("iframe#myFrame3")
