from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.tiktok.com/@startrek?lang=en"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    print(sb.get_text('h2[data-e2e="user-bio"]'))
    for i in range(54):
        sb.cdp.scroll_down(12)
    sb.sleep(1)
