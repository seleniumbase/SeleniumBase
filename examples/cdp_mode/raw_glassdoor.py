from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.glassdoor.com/Reviews/index.htm"
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()
    sb.highlight('[data-test="global-nav-glassdoor-logo"]')
    sb.highlight('[data-test="site-header-companies"]')
    sb.highlight('[data-test="search-button"]')
    sb.highlight('[data-test="sign-in-button"]')
    sb.highlight('[data-test="company-search-autocomplete"]')
