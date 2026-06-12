"""An example of handling alerts in CDP Mode."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://the-internet.herokuapp.com/javascript_alerts")
    sb.click('button[onclick="jsAlert()"]')
    sb.sleep(1)
    sb.uc_gui_press_key("\n")  # Accept Alert
    sb.sleep(1)
    sb.click('button[onclick="jsConfirm()"]')
    sb.sleep(1)
    sb.uc_gui_press_key("ESC")  # Dismiss Alert
    sb.sleep(1)
    sb.click('button[onclick="jsPrompt()"]')
    sb.sleep(1)
    sb.uc_gui_write("Here is my prompt answer\n")
    sb.sleep(1)
