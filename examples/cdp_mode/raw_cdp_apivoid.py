from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.apivoid.com/tools/bot-detection-test/")
sb.highlight('span:contains("Likely Human")')
sb.highlight('span:contains("Tampered: No")')
sb.highlight('span:contains("Triggered rules: 0")')
sb.highlight('#scoreNum:contains("0")')
