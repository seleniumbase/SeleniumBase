"""Context Manager Tests. Can be run with pure "python". (pytest not needed)"""
from seleniumbase import SB

with SB(test=True) as sb:
    sb.open("https://google.com/ncr")
    sb.type('[name="q"]', "SeleniumBase on GitHub\n")
    sb.click('a[href*="github.com/seleniumbase"]')
    sb.highlight("div.Layout-main")
    sb.highlight("div.Layout-sidebar")
    sb.sleep(0.5)

with SB(test=True, rtf=True, demo=True) as sb:
    sb.open("seleniumbase.github.io/demo_page")
    sb.type("#myTextInput", "This is Automated")
    sb.assert_text("This is Automated", "#myTextInput")
    sb.assert_text("This Text is Green", "#pText")
    sb.click('button:contains("Click Me")')
    sb.assert_text("This Text is Purple", "#pText")
    sb.click("#checkBox1")
    sb.assert_element_not_visible("div#drop2 img#logo")
    sb.drag_and_drop("img#logo", "div#drop2")
    sb.assert_element("div#drop2 img#logo")
