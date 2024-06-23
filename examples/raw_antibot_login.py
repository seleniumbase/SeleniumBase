"""UC Mode has PyAutoGUI methods for CAPTCHA-bypass."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://seleniumbase.io/antibot/login"
    sb.uc_open_with_disconnect(url, 2.15)
    sb.uc_gui_write("\t" + "demo_user")
    sb.uc_gui_write("\t" + "secret_pass")
    sb.uc_gui_press_keys("\t" + " ")  # For Single-char keys
    sb.sleep(1.5)
    sb.uc_gui_press_keys(["\t", "ENTER"])  # Multi-char keys
    sb.reconnect(1.8)
    sb.assert_text("Welcome!", "h1")
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
