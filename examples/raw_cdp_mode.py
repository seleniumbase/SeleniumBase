"""CDP Mode for evading bot-detection."""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://browserscan.net/bot-detection")
sb.assert_element('strong:contains("Normal")')
sb.sleep(1)
sb.get("https://bot.sannysoft.com/")
sb.assert_element(".passed")
sb.assert_element_not_visible(".failed")
sb.sleep(1)
sb.quit()
