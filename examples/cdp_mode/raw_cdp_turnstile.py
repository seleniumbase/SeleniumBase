from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://seleniumbase.io/apps/turnstile")
sb.solve_captcha()
sb.assert_element("img#captcha-success")
sb.set_messenger_theme(location="top_left")
sb.post_message("SeleniumBase wasn't detected", duration=3)
sb.quit()
