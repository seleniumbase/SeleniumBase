"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True, pls="none") as sb:
    url = "https://socialblade.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(1.5)
    if not sb.is_element_visible('input[placeholder*="Search"]'):
        sb.solve_captcha()
        sb.sleep(0.5)
    channel_name = "michaelmintz"
    channel_title = "Michael Mintz"
    sb.press_keys('input[placeholder*="Search"]', channel_name)
    sb.sleep(2)
    sb.click('a:contains("%s")' % channel_title)
    sb.sleep(2)
    sb.remove_elements("#lngtd-top-sticky")
    sb.sleep(1.5)
    name = sb.get_text("h3")
    ch_name = name.split(" ")[-1]
    name = name.split(" @")[0]
    link = "https://www.youtube.com/%s" % ch_name
    print("********** SocialBlade Stats for %s: **********" % name)
    print(">>> (Link: %s) <<<" % link)
    print(sb.get_text('[class*="grid lg:hidden"]'))
    print("********** SocialBlade Ranks: **********")
    print(sb.get_text('[class*="gap-3 flex-1"]'))
    for i in range(17):
        sb.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
