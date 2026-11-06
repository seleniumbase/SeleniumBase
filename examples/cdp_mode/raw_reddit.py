"""Reddit Search / Bypasses reCAPTCHA."""
from seleniumbase import SB

with SB(uc=True, test=True, use_chromium=True) as sb:
    search = "Reddit Scraping"
    sb.activate_cdp_mode()
    sb.goto("https://www.reddit.com/r/webscraping/")
    sb.solve_captcha()  # Might not be needed
    sb.click("faceplate-search-input")
    sb.press_keys("html", search + "\n")
    sb.sleep(2.5)
    post_title = '[data-testid="post-title"]'
    sb.wait_for_element(post_title)
    for i in range(8):
        sb.scroll_down(25)
        sb.sleep(0.25)
    posts = sb.select_all(post_title)
    print('*** Reddit Posts for "%s":' % search)
    for post in posts:
        print("* " + post.text)
