"""Test that CDP Mode can use XPath selectors."""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://seleniumbase.io/demo_page")
sb.highlight('//input[@id="myTextInput"]')
sb.type('//*[@id="myTextInput"]', "XPath Test!")
sb.sleep(0.5)
sb.highlight('//button[contains(text(),"(Green)")]')
sb.click('//button[starts-with(text(),"Click Me")]')
sb.assert_element('//button[contains(., "Purple")]')
sb.sleep(0.5)
sb.highlight("//table/tbody/tr/td/h3")
sb.highlight("//table/tbody/tr[1]/td[2]/h2")
sb.assert_text("SeleniumBase", "//table//h2")
