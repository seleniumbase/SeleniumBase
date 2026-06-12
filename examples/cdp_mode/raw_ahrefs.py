from seleniumbase import SB

with SB(uc=True, test=True, incognito=True, locale="en") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://ahrefs.com/website-authority-checker")
    search_term = "github.com/seleniumbase/SeleniumBase"
    sb.type('input[placeholder="Enter domain"]', search_term)
    sb.scroll_down(36)
    sb.click('span:contains("Check Authority")')
    sb.sleep(2)
    sb.solve_captcha()
    sb.sleep(3)
    sb.wait_for_text_not_visible("Checking", timeout=15)
    sb.click_if_visible('button[data-cky-tag="close-button"]')
    sb.highlight('p:contains("github.com/seleniumbase/SeleniumBase")')
    sb.highlight('a:contains("Top 100 backlinks")')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
