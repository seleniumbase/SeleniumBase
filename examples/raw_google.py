from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://google.com/ncr"
    sb.activate_cdp_mode(url)
    sb.type('[name="q"]', "SeleniumBase GitHub page")
    sb.click('[value="Google Search"]')
    sb.sleep(4)  # The "AI Overview" sometimes loads
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
