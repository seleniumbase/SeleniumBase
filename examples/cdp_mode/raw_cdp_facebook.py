from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(ad_block=True)
sb.goto("https://www.facebook.com/SeleniumBase")
sb.sleep(3)
sb.click_if_visible('[aria-label="Close"] i', timeout=2)
sb.sleep(1)
sb.click_if_visible('[aria-label="Close"] i')
for i in range(18):
    sb.scroll_down(14)
    sb.sleep(0.12)
print(sb.get_page_title())
sb.save_as_pdf_to_logs()
sb.save_page_source_to_logs()
sb.save_screenshot_to_logs()
print("Logs have been saved to: ./latest_logs/")
sb.quit()
