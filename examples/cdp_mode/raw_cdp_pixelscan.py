from seleniumbase import sb_cdp

url = "https://pixelscan.net/fingerprint-check"
sb = sb_cdp.Chrome(url, incognito=True)
sb.remove_element("#headerBanner")
sb.wait_for_element("pxlscn-dynamic-ad")
sb.sleep(0.5)
sb.remove_elements("pxlscn-dynamic-ad")
sb.sleep(2)
sb.assert_text("No masking detected", "pxlscn-fingerprint-masking")
sb.assert_text("No automated behavior", "pxlscn-bot-detection")
sb.highlight('span:contains("is consistent")')
sb.sleep(1)
sb.highlight("pxlscn-fingerprint-masking p")
sb.sleep(1)
sb.highlight("pxlscn-bot-detection p")
sb.sleep(2)
