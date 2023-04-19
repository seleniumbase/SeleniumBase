"""Context Manager Test. Runs with "python". (pytest not needed)."""
from seleniumbase import SB

with SB() as sb:  # By default, browser="chrome" if not set.
    sb.open("https://seleniumbase.io/realworld/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
    sb.assert_text("Welcome!", "h1")
    sb.highlight("img#image1")  # A fancier assert_element() call
    sb.click('a:contains("This Page")')  # Use :contains() on any tag
    sb.click_link("Sign out")  # Link must be "a" tag. Not "button".
    sb.assert_element('a:contains("Sign in")')
    sb.assert_exact_text("You have been signed out!", "#top_message")
