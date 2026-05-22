from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.lens.org/lens/patent/135-034-272-112-366/frontpage"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    sb.solve_captcha()
    sb.flash('[ng-if*="patent.title"]', duration=3, pause=2)
    print("* " + sb.get_text('[ng-if*="patent.title"]') + " *")
    print(sb.get_text("ol.claims"))
