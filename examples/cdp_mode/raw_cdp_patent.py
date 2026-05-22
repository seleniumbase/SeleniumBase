from seleniumbase import sb_cdp

url = "https://www.lens.org/lens/patent/135-034-272-112-366/frontpage"
sb = sb_cdp.Chrome(url)
sb.sleep(3.5)
sb.solve_captcha()
sb.flash('[ng-if*="patent.title"]', duration=3, pause=2)
print("* " + sb.get_text('[ng-if*="patent.title"]') + " *")
print(sb.get_text("ol.claims"))
