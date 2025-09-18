from seleniumbase import SB

with SB(test=True, uc=True) as sb:
    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "SeleniumBase GitHub page")
    sb.click("div:not([jsname]) > * > input")
    print(sb.get_page_title())
    sb.sleep(2)  # Wait for the "AI Overview" result
    if sb.is_text_visible("Generating"):
        sb.wait_for_text("AI Overview")
    sb.save_as_pdf_to_logs()  # Saved to ./latest_logs/
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
