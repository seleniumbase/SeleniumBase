from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CDPNetworkBlockingTests(BaseCase):
    def test_cdp_network_blocking(self):
        self.open("about:blank")
        if self._reuse_session or not self.is_chromium():
            message = "Skipping test if reusing session or not Chromium!"
            print(message)
            self.skip(message)
        self.execute_cdp_cmd("Network.enable", {})
        self.execute_cdp_cmd(
            "Network.setBlockedURLs", {"urls": [
                "*.googlesyndication.com*",
                "*.googletagmanager.com*",
                "*.google-analytics.com*",
                "*.amazon-adsystem.com*",
                "*.adsafeprotected.com*",
                "*.doubleclick.net*",
                "*.fastclick.net*",
                "*.snigelweb.com*",
                "*.2mdn.net*",
            ]})
        self.open("https://www.w3schools.com/jquery/default.asp")
        source = self.get_page_source()
        self.assert_false("doubleclick.net" in source)
        self.assert_false("google-analytics.com" in source)
        self.post_message("Blocking was successful!")
