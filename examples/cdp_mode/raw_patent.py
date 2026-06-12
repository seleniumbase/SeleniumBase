from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.lens.org/lens/patent/135-034-272-112-366/frontpage")
    sb.sleep(4)
    sb.solve_captcha()
    sb.flash('[ng-if*="patent.title"]', duration=3, pause=2)
    print("* " + sb.get_text('[ng-if*="patent.title"]') + " *")
    print(sb.get_text("ol.claims"))
