from seleniumbase import sb_cdp

url = "https://www.browserscan.net/bot-detection"
sb = sb_cdp.Chrome(url, locale="en", ad_block=True)
sb.flash("Test Results", duration=3, pause=1)
sb.assert_element('strong:contains("Normal")')
print("Bot Not detected")
sb.flash('strong:contains("Normal")', duration=3, pause=2)
