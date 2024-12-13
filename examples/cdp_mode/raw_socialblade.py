"""Bypass bot-detection to view SocialBlade ranks for YouTube"""
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True, pls="none") as sb:
    url = "https://socialblade.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(1.5)
    sb.uc_gui_click_captcha()
    sb.sleep(0.5)
    channel_name = "michaelmintz"
    sb.cdp.press_keys('input[name="query"]', channel_name)
    sb.cdp.click('form[action*="/search"] button')
    sb.sleep(2)
    sb.cdp.click('a[title="%s"] h2' % channel_name)
    sb.sleep(1.5)
    sb.cdp.remove_elements("#lngtd-top-sticky")
    sb.sleep(1.5)
    name = sb.cdp.get_text("h1")
    link = sb.cdp.get_attribute("#YouTubeUserTopInfoBlockTop h4 a", "href")
    subscribers = sb.cdp.get_text("#youtube-stats-header-subs")
    video_views = sb.cdp.get_text("#youtube-stats-header-views")
    rankings = sb.cdp.get_text(
        '#socialblade-user-content [style*="border-bottom"]'
    ).replace("\xa0", "").replace("   ", " ").replace("  ", " ")
    print("********** SocialBlade Stats for %s: **********" % name)
    print(">>> (Link: %s) <<<" % link)
    print("* YouTube Subscribers: %s" % subscribers)
    print("* YouTube Video Views: %s" % video_views)
    print("********** SocialBlade Ranks: **********")
    for row in rankings.split("\n"):
        if len(row.strip()) > 8:
            print("-->  " + row.strip())
    for i in range(17):
        sb.cdp.scroll_down(6)
        sb.sleep(0.1)
    sb.sleep(2)
