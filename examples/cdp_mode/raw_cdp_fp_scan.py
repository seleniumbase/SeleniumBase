from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://fingerprint-scan.com/")
sb.wait_for_text("Fingerprint collected successfully")
print(sb.get_text('span:contains("Bot score")'))
if sb.headed:
    sb.sleep(2)  # Slow down for the live demo
