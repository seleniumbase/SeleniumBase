"""Reddit Search / Bypasses reCAPTCHA."""
from seleniumbase import SB

with SB(uc=True, test=True, use_chromium=True) as sb:
    search = "reddit+scraper"
    url = f"https://www.reddit.com/r/webscraping/search/?q={search}"
    sb.activate_cdp_mode(url)
    sb.solve_captcha()  # Might not be needed
    post_title = '[data-testid="post-title"]'
    sb.wait_for_element(post_title)
    for i in range(8):
        sb.scroll_down(25)
        sb.sleep(0.2)
    posts = sb.select_all(post_title)
    print('*** Reddit Posts for "%s":' % search)
    for post in posts:
        print("* " + post.text)
