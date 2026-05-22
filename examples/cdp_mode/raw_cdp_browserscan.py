from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", ad_block=True)
sb.open("https://browserscan.net/bot-detection")
sb.flash("Test Results", duration=1.5, pause=0.5)
sb.assert_element('strong:contains("Normal")')
print("Bot Not Detected")
sb.flash('strong:contains("Normal")', pause=1)
