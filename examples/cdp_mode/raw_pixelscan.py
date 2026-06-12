from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode(ad_block=True)
    sb.goto("https://pixelscan.net/fingerprint-check")
    sb.sleep(1.5)
    sb.wait_for_element("pxlscn-dynamic-ad")
    sb.sleep(0.5)
    sb.remove_elements("pxlscn-dynamic-ad")
    sb.sleep(1.5)
    sb.assert_text("No automated behavior", "pxlscn-bot-detection")
    sb.wait_for_element("span.status-success")
    sb.assert_text("No masking detected", "pxlscn-fingerprint-masking")
    sb.cdp.highlight("span.status-success")
    sb.cdp.highlight("pxlscn-fingerprint-masking p")
    sb.cdp.highlight("pxlscn-bot-detection p")
    print("Bot Not Detected")
