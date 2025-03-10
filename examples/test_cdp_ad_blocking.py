from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CDPNetworkBlockingTests(BaseCase):
    def test_cdp_network_blocking(self):
        self.open("about:blank")
        if self._reuse_session or not self.is_chromium():
            message = "Skipping test if reusing session or not Chromium!"
            print(message)
            self.skip(message)
        self.execute_cdp_cmd(
            'Network.setBlockedURLs', {"urls": [
                "*googlesyndication.com*",
                "*doubleclick.net*",
                "*adsafeprotected.com*",
                "*2mdn.net*",
                "*googletagmanager.com*",
                "*adsafeprotected.com*",
                "*snigelweb.com*",
                "*fastclick.net*",
                "*amazon-adsystem.com*",
                "*google-analytics.com*",
            ]})
        self.execute_cdp_cmd('Network.enable', {})
        self.open('https://www.w3schools.com/jquery/default.asp')
        self.ad_block()
        source = self.get_page_source()
        self.assert_true("doubleclick.net" not in source)
        self.assert_true("google-analytics.com" not in source)
        self.post_message("Blocking was successful!")
