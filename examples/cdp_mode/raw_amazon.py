from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.amazon.com"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.click_if_visible('button[alt="Continue shopping"]')
    sb.sleep(2)
    sb.press_keys('input[role="searchbox"]', "TI-89\n")
    sb.sleep(3)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
