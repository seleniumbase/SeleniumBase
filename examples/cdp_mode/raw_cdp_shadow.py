"""An example of displaying Shadow DOM inside HTML"""
from seleniumbase import sb_cdp

url = "https://seleniumbase.io/apps/turnstile"
sb = sb_cdp.Chrome(url)
element = sb.find_element("div.cf-turnstile div")
html_with_shadow_dom = element.get_html()
print(html_with_shadow_dom)
text_to_find = "Widget containing a Cloudflare security challenge"
sb.assert_true(text_to_find in html_with_shadow_dom)
sb.solve_captcha()
sb.assert_element("img#captcha-success", timeout=3)
sb.set_messenger_theme(location="top_left")
sb.post_message("SeleniumBase wasn't detected", duration=3)
