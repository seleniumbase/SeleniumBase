from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://bot.sannysoft.com/")
    sb.flash("#user-agent-result.passed")
    sb.flash("#webdriver-result.passed")
    sb.flash("#advanced-webdriver-result.passed")
    sb.flash("#chrome-result.passed")
    sb.flash("#permissions-result.passed")
    sb.flash("#plugins-length-result.passed")
    sb.flash("#plugins-type-result.passed")
    sb.flash("#languages-result.passed")
    sb.flash("#webgl-vendor.passed")
    sb.flash("#webgl-renderer.passed")
    sb.flash("#broken-image-dimensions.passed")
    print("Bot Not Detected")
    sb.sleep(1)
