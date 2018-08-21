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
    '[href*="doubleclick.net/"]',
    '[id*="-ad-"]',
    '[id*="_ads_"]',
    '[id*="AdFrame"]',
    '[id*="carbonads"]',
    '[id^="ad-"]',
    '[id^="outbrain_widget"]',
    '[id^="taboola-"]',
    '[id="dianomiRightRail"]',
    '[src*="smartads."]',
    '[src*="ad_nexus"]',
    '[src*="/ads/"]',
    '[data-dcm-click-tracker*="/adclick."]',
    '[data-google-query-id^="C"]',
    'div.ad-container',
    'div.ad_module',
    'div.ad-subnav-container',
    'div.ad-wrapper',
    'div.data-ad-container',
    'div.l-ad',
    'div.right-ad',
    'div.wx-adWrapper',
    'img.img_ad',
    'link[href*="/adservice."]',
    'script[src*="/adservice."]',
    'script[src*="/pagead/"]',
    'section.dianomi-ad',
]
