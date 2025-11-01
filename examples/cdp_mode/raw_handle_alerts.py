"""An example of handling alerts in CDP Mode."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    sb.activate_cdp_mode(url)
    sb.cdp.gui_click_element('button[onclick="jsAlert()"]')
    sb.sleep(1)
    sb.uc_gui_press_key("\n")  # Accept Alert
    sb.sleep(1)
    sb.cdp.gui_click_element('button[onclick="jsConfirm()"]')
    sb.sleep(1)
    sb.uc_gui_press_key("ESC")  # Dismiss Alert
    sb.sleep(1)
    sb.cdp.gui_click_element('button[onclick="jsPrompt()"]')
    sb.sleep(1)
    sb.uc_gui_write("Here is my prompt answer\n")
    sb.sleep(1)
