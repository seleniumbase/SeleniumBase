from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
sb.goto("https://gitlab.com/users/sign_in")
sb.sleep(2)
sb.solve_captcha()
sb.highlight('h1:contains("GitLab")')
sb.highlight('button:contains("Sign in")')
sb.quit()
