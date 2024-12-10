from seleniumbase import SB

with SB(uc=True, incognito=True, test=True) as sb:
    sb.activate_cdp_mode("https://pixelscan.net/")
    sb.sleep(3)
    sb.remove_elements("div.banner")  # Remove the banner
    sb.remove_elements("jdiv")  # Remove chat widgets
    sb.cdp.scroll_down(15)
    not_masking_text = "You are not masking your fingerprint"
    sb.assert_text(not_masking_text, "pxlscn-fingerprint-masking")
    no_automation_detected = "No automation framework detected"
    sb.assert_text(no_automation_detected, "pxlscn-bot-detection")
    sb.highlight("span.text-success", loops=8)
    sb.sleep(1)
    fingerprint_masking_div = "pxlscn-fingerprint-masking div"
    sb.highlight(fingerprint_masking_div, loops=9)
    sb.sleep(1)
    sb.highlight(".bot-detection-context", loops=10)
    sb.sleep(2)
