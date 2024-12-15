from seleniumbase import SB

with SB(test=True, ad_block=True, locale_code="en") as sb:
    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "SeleniumBase GitHub page\n")
    sb.click('[href*="github.com/seleniumbase/SeleniumBase"]')
    sb.save_screenshot_to_logs()  # (See ./latest_logs folder)
    print(sb.get_page_title())
