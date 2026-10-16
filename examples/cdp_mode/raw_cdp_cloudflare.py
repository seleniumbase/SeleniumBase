from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://dash.cloudflare.com/sign-up")
sb.sleep(3)
sb.solve_captcha()
sb.sleep(3)
cookie_value = None
for cookie in sb.get_all_cookies():
    if cookie.name == "cf_clearance":
        cookie_value = cookie.value
        break
if cookie_value:
    print("cf_clearance cookie: %s" % cookie_value)
else:
    print("Didn't find the cf_clearance cookie!")
sb.quit()
