from seleniumbase import SB

with SB(uc=True, incognito=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("https://pixelscan.net/", 10)
    sb.remove_elements("jdiv")  # Remove chat widgets
    no_automation_detected = "No automation framework detected"
    sb.assert_text(no_automation_detected, "pxlscn-bot-detection")
    not_masking_text = "You are not masking your fingerprint"
    sb.assert_text(not_masking_text, "pxlscn-fingerprint-masking")
    sb.highlight("span.text-success", loops=8)
    sb.sleep(1)
    fingerprint_masking_div = "pxlscn-fingerprint-masking div"
    sb.highlight(fingerprint_masking_div, loops=9, scroll=False)
    sb.sleep(1)
    sb.highlight(".bot-detection-context", loops=10, scroll=False)
    sb.sleep(2)
