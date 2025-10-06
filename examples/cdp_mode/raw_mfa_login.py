from seleniumbase import sb_cdp

url = "https://seleniumbase.io/realworld/login"
sb = sb_cdp.Chrome(url)
sb.type("#username", "demo_user")
sb.type("#password", "secret_pass")
sb.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")
sb.assert_text("Welcome!", "h1")
sb.click('a:contains("This Page")')
sb.highlight("h1")
sb.highlight("img#image1")
sb.driver.stop()
