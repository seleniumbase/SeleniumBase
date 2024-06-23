"""If Brotector catches you, Gandalf blocks you!"""
from seleniumbase import SB

with SB(test=True) as sb:
    url = "https://seleniumbase.io/hobbit/login"
    sb.open(url)
    sb.click_if_visible("button")
    sb.assert_text("Gandalf blocked you!", "h1")
    sb.click("img")
    sb.highlight("h1")
    sb.sleep(3)  # Gandalf: "You Shall Not Pass!"
