from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://google.com/ncr")
    sb.click_if_visible('button:contains("Accept all")')
    sb.press_keys('[name="q"]', "SeleniumBase GitHub page\n")
    sb.sleep(4)  # The "AI Overview" sometimes loads
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
