from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode(ad_block=True)
    sb.goto("https://pixelscan.net/fingerprint-check")
    sb.remove_element("div.header-ad")
    sb.remove_element("pxlscn-dynamic-ad")
    sb.sleep(1.8)
    sb.assert_text("No automated behavior", "pxlscn-bot-detection")
    sb.assert_text("No masking detected", "pxlscn-fingerprint-masking")
    sb.assert_text("consistent", "span.status-success")
    sb.sleep(0.5)
    sb.cdp.highlight("span.status-success")
    sb.cdp.highlight("pxlscn-fingerprint-masking p")
    sb.cdp.highlight("pxlscn-bot-detection p")
    print("Bot Not Detected")
