from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.cloudflare.com/login"
    sb.activate_cdp_mode(url)
    sb.wait_for_element('div[data-testid*="challenge-widget"]')
    sb.sleep(1.5)
    sb.solve_captcha()
    sb.sleep(3)
