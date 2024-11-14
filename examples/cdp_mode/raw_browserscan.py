from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.browserscan.net/bot-detection"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.cdp.flash("Test Results", duration=4)
    sb.sleep(1)
    sb.cdp.assert_element('strong:contains("Normal")')
    sb.cdp.flash('strong:contains("Normal")', duration=4, pause=4)
