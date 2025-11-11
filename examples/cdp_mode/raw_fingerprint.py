from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://demo.fingerprint.com/playground"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.cdp.highlight('a[href*="browser-bot-detection"]')
    bot_row_selector = 'table:contains("Bot") tr:nth-of-type(3)'
    print(sb.get_text(bot_row_selector))
    sb.assert_text("Bot Not detected", bot_row_selector)
    sb.cdp.highlight(bot_row_selector)
    sb.sleep(2)
