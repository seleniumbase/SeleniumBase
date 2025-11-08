from seleniumbase import sb_cdp


def get_cf_clearance_cookie(sb):
    all_cookies = sb.get_all_cookies()
    for cookie in all_cookies:
        if cookie.name == "cf_clearance":
            return cookie
    return None


url = "https://gitlab.com/users/sign_in"
sb = sb_cdp.Chrome(url)
sb.sleep(2.5)  # Wait for CAPTCHA to load
sb.solve_captcha()  # (Only if found)
sb.sleep(2.2)  # Wait for CAPTCHA success
cf_cookie = get_cf_clearance_cookie(sb)
if cf_cookie:
    print("cf_clearance cookie: %s" % cf_cookie.value)
else:
    print("Didn't find the cf_clearance cookie!")
sb.driver.stop()
