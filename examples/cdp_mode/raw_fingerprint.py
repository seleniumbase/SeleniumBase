from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://demo.fingerprint.com/playground")
    sb.flash('a[href*="browser-bot-detection"]', duration=3, pause=1)
    bot_row_selector = 'table:contains("Bot") tr:nth-of-type(3)'
    print(sb.get_text(bot_row_selector))
    sb.assert_text("Bot Not detected", bot_row_selector)
    sb.flash(bot_row_selector, duration=3, pause=2)
