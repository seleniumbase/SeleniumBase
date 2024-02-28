from seleniumbase import SB

with SB(uc=True, incognito=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("https://pixelscan.net/", 11)
    sb.remove_elements("jdiv")  # Remove chat widgets
    sb.assert_text("No automation framework detected", "pxlscn-bot-detection")
    sb.assert_text("You are not masking your fingerprint")
    sb.highlight("span.text-success", loops=10)
    sb.sleep(1)
    sb.highlight("pxlscn-fingerprint-masking div", loops=10, scroll=False)
    sb.sleep(1)
    sb.highlight("div.bot-detection-context", loops=10, scroll=False)
    sb.sleep(3)
