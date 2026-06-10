from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://seleniumbase.io/apps/brotector")
    sb.click("button span#mySpan")
    sb.assert_text("SUCCESS", "label#pText")
    sb.highlight("label#pText")
