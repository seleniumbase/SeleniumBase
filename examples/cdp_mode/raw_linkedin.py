from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.linkedin.com/company/selenium"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.click_if_visible('button[aria-label="Dismiss"]')
    sb.sleep(1)
    for i in range(42):
        sb.cdp.scroll_down(16)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
