"""To handle alerts in CDP Mode, reconnect and use WebDriver."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    sb.activate_cdp_mode(url)
    sb.reconnect()
    sb.cdp.gui_click_element('button[onclick="jsAlert()"]')
    sb.sleep(1)
    sb.accept_alert()
    sb.sleep(1)
    sb.cdp.gui_click_element('button[onclick="jsConfirm()"]')
    sb.sleep(1)
    sb.dismiss_alert()
    sb.sleep(1)
    sb.cdp.gui_click_element('button[onclick="jsPrompt()"]')
    sb.sleep(1)
    sb.uc_gui_write("Here is my prompt answer\n")
    sb.sleep(1)
