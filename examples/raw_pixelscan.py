from seleniumbase import SB

with SB(uc=True, incognito=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("https://pixelscan.net/", 10)
    sb.remove_elements("jdiv")  # Remove chat widgets
    sb.assert_text("No automation framework detected", "pxlscn-bot-detection")
    not_masking = "You are not masking your fingerprint"
    sb.assert_text(not_masking, "pxlscn-fingerprint-masking")
    sb.highlight("span.text-success", loops=8)
    sb.sleep(1)
    sb.highlight("pxlscn-fingerprint-masking div", loops=9, scroll=False)
    sb.sleep(1)
    sb.highlight("div.bot-detection-context", loops=10, scroll=False)
    sb.sleep(2)
