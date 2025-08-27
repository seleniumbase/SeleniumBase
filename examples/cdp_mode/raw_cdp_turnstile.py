from seleniumbase import sb_cdp

url = "https://seleniumbase.io/apps/turnstile"
sb = sb_cdp.Chrome(url)
sb.gui_click_captcha()
sb.assert_element("img#captcha-success")
sb.sleep(2)
sb.driver.stop()
