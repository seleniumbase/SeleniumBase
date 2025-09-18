from seleniumbase import sb_cdp

url = "https://gitlab.com/users/sign_in"
sb = sb_cdp.Chrome(url)
sb.sleep(2.5)
sb.gui_click_captcha()
sb.highlight('h1:contains("GitLab.com")')
sb.highlight('button:contains("Sign in")')
sb.driver.stop()
