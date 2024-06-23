"""The Brotector CAPTCHA in action."""
from seleniumbase import SB

with SB(test=True) as sb:
    sb.open("https://seleniumbase.io/antibot/login")
    sb.highlight("h4", loops=6)
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.click_if_visible("button span")
    sb.highlight("label#pText")
    sb.highlight("table#detections")
    sb.sleep(4.4)  # Add time to read the table
