from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://demo.fingerprint.com/playground")
sb.wait_for_element('a[href*="browser-bot-detection"]')
sb.flash('a[href*="browser-bot-detection"]', duration=3, pause=1)
bot_row_selector = 'table:contains("Bot") tr:nth-of-type(3)'
print(sb.get_text(bot_row_selector))
sb.flash(bot_row_selector, duration=3, pause=2)
