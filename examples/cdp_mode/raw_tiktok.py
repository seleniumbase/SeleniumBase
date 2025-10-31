from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.tiktok.com/@startrek?lang=en"
    sb.activate_cdp_mode(url)
    sb.sleep(3)
    print(sb.get_text('h2[data-e2e="user-bio"]'))
    for i in range(54):
        sb.scroll_down(12)
    sb.sleep(1)
