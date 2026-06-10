from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://browserscan.net/bot-detection")
    sb.flash("Test Results", duration=1.5, pause=0.5)
    sb.assert_element('strong:contains("Normal")')
    print("Bot Not Detected")
    sb.flash('strong:contains("Normal")', pause=1)
