from seleniumbase import sb_cdp

url = "https://gitlab.com/users/sign_in"
sb = sb_cdp.Chrome(url, incognito=True)
sb.sleep(2)
sb.solve_captcha()
sb.highlight('h1:contains("GitLab")')
sb.highlight('button:contains("Sign in")')
sb.driver.stop()
