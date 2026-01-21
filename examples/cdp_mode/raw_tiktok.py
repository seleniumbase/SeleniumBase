from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://www.tiktok.com/@startrek?lang=en"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.click_if_visible('button[data-close-button="true"]')
    print("*** " + sb.get_text('h2[data-e2e="user-bio"]'))
    for i in range(33):
        sb.scroll_by_y(33)
        sb.sleep(0.03)
    items = sb.find_elements("picture img")
    for i, item in enumerate(items):
        print("* %s: %s" % (i, str(item.get_attribute("alt"))))
    print("*** %s total items found!" % len(items))
    sb.sleep(1)
