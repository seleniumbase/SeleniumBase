from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://www.glassdoor.com/Reviews/index.htm"
    sb.activate_cdp_mode(url)
    sb.sleep(2.1)
    sb.solve_captcha()
    sb.sleep(0.6)
    sb.highlight('[data-test="global-nav-glassdoor-logo"]')
    sb.highlight('[data-test="site-header-companies"]')
    sb.highlight('[data-test="search-button"]')
    sb.highlight('[data-test="sign-in-button"]')
    sb.highlight('[data-test="company-search-autocomplete"]')
    sb.press_keys("#employer-autocomplete", "NASA Goddard\n")
    sb.sleep(0.5)
    sb.click('button[data-role-variant="primary"] span:contains("Search")')
    sb.sleep(2)
    sb.click('[aria-label*="NASA"] img')
    sb.sleep(2)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
