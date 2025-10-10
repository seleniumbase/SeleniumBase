"""Test that CDP Mode can autodetect and use XPath selectors."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/demo_page"
    sb.activate_cdp_mode(url)
    sb.cdp.highlight('//input[@id="myTextInput"]')
    sb.cdp.type('//*[@id="myTextInput"]', "XPath Test!")
    sb.sleep(0.5)
    sb.cdp.highlight('//button[contains(text(),"(Green)")]')
    sb.cdp.click('//button[starts-with(text(),"Click Me")]')
    sb.cdp.assert_element('//button[contains(., "Purple")]')
    sb.sleep(0.5)
    sb.cdp.highlight("//table/tbody/tr/td/h3")
    sb.cdp.highlight("//table/tbody/tr[1]/td[2]/h2")
    sb.cdp.assert_text("SeleniumBase", "//table//h2")
