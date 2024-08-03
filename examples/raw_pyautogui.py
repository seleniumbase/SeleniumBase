import sys
from seleniumbase import SB

# An incomplete UserAgent forces CAPTCHA-solving on macOS
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0"
if "linux" in sys.platform or "win32" in sys.platform:
    agent = None  # Use the default UserAgent

with SB(uc=True, test=True, rtf=True, agent=agent) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.uc_open_with_reconnect(url, 4)
    sb.uc_gui_handle_captcha()  # Only if needed
    sb.assert_element('label[for="user_login"]')
    sb.assert_element('input[data-testid*="username"]')
    sb.assert_element('input[data-testid*="password"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
