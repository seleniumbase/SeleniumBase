"""
UC Mode now has uc_gui_handle_cf(), which uses PyAutoGUI.
An incomplete UserAgent is used to force CAPTCHA-solving.
"""
import sys
from seleniumbase import SB

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0"
if "linux" in sys.platform:
    agent = None  # Use the default UserAgent

with SB(uc=True, test=True, rtf=True, agent=agent) as sb:
    url = "https://www.virtualmanager.com/en/login"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_handle_cf()  # Ready if needed!
    sb.assert_element('input[name*="email"]')
    sb.assert_element('input[name*="login"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
