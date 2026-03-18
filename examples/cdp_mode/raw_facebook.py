from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.facebook.com/SeleniumBase"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.click_if_visible('[aria-label="Close"] i')
    sb.sleep(1)
    for i in range(16):
        sb.cdp.scroll_down(16)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
