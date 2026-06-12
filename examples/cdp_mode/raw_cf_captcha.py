from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.cloudflare.com/login")
    sb.wait_for_element('div[data-testid*="challenge-widget"]')
    sb.sleep(2.5)
    sb.solve_captcha()
    sb.sleep(3)
