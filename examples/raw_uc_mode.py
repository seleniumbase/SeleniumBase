"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("https://top.gg/", 5)
    if not sb.is_text_visible("Discord Bots", "h1"):
        sb.driver.uc_open_with_reconnect("https://top.gg/", 5)
    sb.assert_text("Discord Bots", "h1", timeout=3)
    sb.highlight("h1", loops=3)
    sb.set_messenger_theme(location="top_center")
    sb.post_message("Selenium wasn't detected!", duration=3)
