from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True)
sb.goto("https://google.com/ncr")
sb.click_if_visible('button:contains("Accept all")')
sb.press_keys('[name="q"]', "SeleniumBase GitHub Page")
sb.sleep(0.5)
if sb.is_element_visible('[value="Google Search"]'):
    sb.click('[value="Google Search"]')
else:
    sb.press_keys('[name="q"]', "\n")
sb.sleep(1)
sb.click_if_visible('h3:contains("seleniumbase/SeleniumBase")')
sb.sleep(1)
print(sb.get_page_title())
sb.save_as_pdf("seleniumbase.pdf", folder="./downloaded_files/")
print("* PDF saved to ./downloaded_files/seleniumbase.pdf")
sb.quit()
