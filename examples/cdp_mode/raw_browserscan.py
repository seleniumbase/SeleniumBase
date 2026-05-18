from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.browserscan.net/bot-detection"
    sb.activate_cdp_mode(url)
    sb.cdp.flash("Test Results", duration=3, pause=1)
    sb.assert_element('strong:contains("Normal")')
    print("Bot Not detected")
    sb.cdp.flash('strong:contains("Normal")', duration=3, pause=2)
