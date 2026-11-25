from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.apivoid.com/tools/bot-detection-test/")
risk_score = sb.get_numeric_text("#scoreNum")
print(f"Risk Score (lower is better): {risk_score}")
sb.scroll_into_view("#scoreNum")
if sb.headed:
    sb.sleep(2)  # Slow down for the live demo
sb.save_screenshot("./downloaded_files/apivoid.png")
sb.save_as_pdf("./downloaded_files/pdf_apivoid.pdf")
