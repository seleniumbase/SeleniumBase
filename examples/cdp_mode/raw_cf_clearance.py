from seleniumbase import sb_cdp

url = "https://gitlab.com/users/sign_in"
sb = sb_cdp.Chrome(url)
sb.sleep(2.2)
sb.gui_click_captcha()
sb.sleep(2)
cf_cookie = None
all_cookies = sb.get_all_cookies()
for cookie in all_cookies:
    if cookie.name == 'cf_clearance':
        cf_cookie = cookie
        break
if cf_cookie:
    print("cf_clearance cookie: %s" % cf_cookie.value)
else:
    print("Didn't find the cf_clearance cookie!")
sb.driver.stop()
