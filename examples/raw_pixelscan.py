from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://pixelscan.net/fingerprint-check"
    sb.activate_cdp_mode(url)
    sb.wait_for_element("pxlscn-dynamic-ad")
    sb.sleep(0.5)
    sb.remove_elements("pxlscn-dynamic-ad")
    sb.sleep(2)
    sb.assert_text("No masking detected", "pxlscn-fingerprint-masking")
    sb.assert_text("No automated behavior", "pxlscn-bot-detection")
    sb.cdp.highlight('span.status-success')
    sb.sleep(1)
    sb.cdp.highlight("pxlscn-fingerprint-masking p")
    sb.sleep(1)
    sb.cdp.highlight("pxlscn-bot-detection p")
    sb.sleep(2)
