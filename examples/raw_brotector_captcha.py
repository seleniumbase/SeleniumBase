"""UC Mode has PyAutoGUI methods for CAPTCHA-bypass."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/apps/brotector"
    sb.uc_open_with_disconnect(url, 2.2)
    sb.uc_gui_press_key("\t")
    sb.uc_gui_press_key(" ")
    sb.reconnect(2.2)
