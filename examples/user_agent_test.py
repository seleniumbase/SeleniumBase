from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class UserAgentTests(BaseCase):
    def test_user_agent(self):
        self.open("http://whatsmyuseragent.org/")
        user_agent_detected = self.get_text(".user-agent p")
        original_user_agent = user_agent_detected
        if not self.user_agent:
            # Using the built-in user-agent string
            print("\n\nUser-Agent: %s" % user_agent_detected)
        else:
            # User-agent was overridden using: --agent=STRING
            print("\n\nUser-Agent override: %s" % user_agent_detected)
        print("\n" + self.get_text(".ip-address p"))
        if not (self.headless or self.headless2 or self.xvfb):
            self.sleep(3)

        # Now change the user-agent using "execute_cdp_cmd()"
        if not self.is_chromium():
            msg = "\n* execute_cdp_cmd() is only for Chromium browsers"
            print(msg)
            self.skip(msg)
        print("\n--------------------------")
        try:
            self.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {
                    "userAgent": "Mozilla/5.0 "
                    "(Nintendo Switch; WifiWebAuthApplet) "
                    "AppleWebKit/606.4 (KHTML, like Gecko) "
                    "NF/6.0.1.15.4 NintendoBrowser/5.1.0.20393"
                },
            )
            self.open("http://whatsmyuseragent.org/")
            user_agent_detected = self.get_text(".user-agent p")
            print("\nUser-Agent override: %s" % user_agent_detected)
            print("\n" + self.get_text(".ip-address p") + "\n")
            if not (self.headless or self.headless2 or self.xvfb):
                self.sleep(3)
        finally:
            # Reset the user-agent back to the original
            self.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": original_user_agent},
            )
