"""
For use with SeleniumBase ad_block functionality.

Usage:
    On the command line:
    "pytest SOME_TEST.py --ad_block"

    From inside a test:
    self.ad_block()

If using the command line version, the ad_block functionality gets
activated after "self.wait_for_ready_state_complete()" is called,
which is always run after page loads, unless changed in "settings.py".
Using ad_block will slow down test runs a little. (Use only if necessary.)

Format: A CSS Selector that's ready for JavaScript's querySelectorAll()
"""

AD_BLOCK_LIST = [
    '[aria-label="Ad"]',
    '[class^="sponsored-content"]',
    '[data-ad-details*="Advertisement"]',
    '[data-native_ad*="placement"]',
    '[data-provider="dianomi"]',
    '[data-type="ad"]',
    '[data-track-event-label*="-taboola-"]',
    '[data-ad-feedback-beacon*="AD_"]',
    '[data-ad-feedback-beacon]',
    '[href*="doubleclick.net/"]',
    '[href*="amazon-adsystem"]',
    '[id*="-ad-"]',
    '[id*="_ads_"]',
    '[alt="Advertisement"]',
    '[id*="AdFrame"]',
    '[id*="carbonads"]',
    '[id^="ad-"]',
    '[id^="my-ads"]',
    '[id^="outbrain_widget"]',
    '[id^="taboola-"]',
    '[id="dianomiRightRail"]',
    '[src*="smartads."]',
    '[src*="ad_nexus"]',
    '[src*="/ads/"]',
    '[data-dcm-click-tracker*="/adclick."]',
    '[data-google-query-id^="C"]',
    '[allow*="advertising.com"]',
    '[data-ylk*="pkgt:sponsored_cluster"]',
    '[data-ad-slot]',
    'iframe[onload*="doWithAds"]',
    'iframe[src*="doubleclick.net"]',
    'iframe[id*="google_ads_frame"]',
    'ins.adsbygoogle',
    'li.strm-ad-clusters',
    'li.js-stream-ad',
    'div.after_ad',
    'div.ad-container',
    'div.ad_module',
    'div.ad-subnav-container',
    'div.ad-wrapper',
    'div.data-ad-container',
    'div.l-ad',
    'div.right-ad',
    'div.wx-adWrapper',
    'div.image > a > img[src*="HomepageAd-"]',
    'img[src*="HomepageAd-"]',
    'img.img_ad',
    'link[href*="/adservice."]',
    'script[src*="/adservice."]',
    'script[type="data-doubleclick"]',
    'script[src*="doubleclick.net"]',
    'script[src*="googletagservices.com/"]',
    'script[src*="ad.doubleclick.net/"]',
    'script[src*="/pagead/"]',
    'section.dianomi-ad',
]
