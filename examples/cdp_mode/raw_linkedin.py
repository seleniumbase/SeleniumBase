from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.linkedin.com/company/selenium")
    sb.sleep(1)
    sb.click_if_visible('button[aria-label="Dismiss"]', timeout=2)
    sb.sleep(0.5)
    for i in range(14):
        sb.scroll_down(48)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
