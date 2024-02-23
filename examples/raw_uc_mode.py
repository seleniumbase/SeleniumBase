"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("https://top.gg/", 4)
    if not sb.is_text_visible("Discord Bots", "h1"):
        sb.get_new_driver(undetectable=True)
        sb.driver.uc_open_with_reconnect("https://top.gg/", 5)
    sb.activate_demo_mode()  # Highlight + show assertions
    sb.assert_text("Discord Bots", "h1", timeout=3)
