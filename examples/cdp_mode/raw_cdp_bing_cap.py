from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.bing.com/turing/captcha/challenge")
sb.solve_captcha()
sb.sleep(2)
