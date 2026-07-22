from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.glassdoor.com/Reviews/index.htm")
    sb.sleep(2.2)
    sb.solve_captcha()
    sb.sleep(0.6)
    sb.highlight('[data-test="global-nav-glassdoor-logo"]')
    sb.highlight('[data-test="site-header-companies"]')
    sb.highlight('[data-test="search-button"]')
    sb.highlight('[data-test="sign-in-button"]')
    sb.highlight('[data-test="company-search-autocomplete"]')
    sb.press_keys("#employer-autocomplete", "NASA Goddard\n")
    sb.sleep(1)
    sb.click_if_visible(
        '[data-role-variant="primary"] span:contains("Search")'
    )
    sb.sleep(1)
    sb.click_if_visible('[aria-label*="NASA"] img')
    sb.sleep(1)
    print(sb.get_page_title())
    sb.save_as_pdf_to_logs()
    sb.save_page_source_to_logs()
    sb.save_screenshot_to_logs()
    print("Logs have been saved to: ./latest_logs/")
