from seleniumbase import SB

with SB(test=True, uc=True) as sb:
    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "SeleniumBase GitHub page\n")
    sb.sleep(1)
    sb.click('[href*="github.com/seleniumbase/"]')
    sb.save_screenshot_to_logs()  # ./latest_logs/
    print(sb.get_page_title())
