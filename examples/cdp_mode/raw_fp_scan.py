from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://fingerprint-scan.com/")
    sb.wait_for_text("Fingerprint collected successfully")
    print(sb.get_text('span:contains("Bot score")'))
    if sb.headed:
        sb.sleep(2)  # Slow down for the live demo
