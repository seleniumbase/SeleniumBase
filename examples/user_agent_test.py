from seleniumbase import BaseCase


class UserAgentTests(BaseCase):
    def test_user_agent(self):
        self.open("https://www.whatsmyua.info/")
        user_agent_detected = self.get_text("#custom-ua-string")
        original_user_agent = user_agent_detected
        if not self.user_agent:
            # Using the built-in user-agent string
            self._print("\n\nUser-Agent = %s\n" % user_agent_detected)
        else:
            # User-agent was overridden using: --agent=STRING
            self._print("\n\nUser-Agent override = %s\n" % user_agent_detected)
        self.sleep(3)

        if not self.is_chromium():
            # Skip the rest of the test if not using a Chromium browser
            msg = "\n* execute_cdp_cmd() is only for Chromium browsers"
            self._print(msg)
            self.skip(msg)
        try:
            # Now change the user-agent using "execute_cdp_cmd()"
            print("--------------------------")
            self.driver.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {
                    "userAgent": "Mozilla/5.0 "
                    "(Nintendo Switch; WifiWebAuthApplet) "
                    "AppleWebKit/606.4 (KHTML, like Gecko) "
                    "NF/6.0.1.15.4 NintendoBrowser/5.1.0.20393"
                },
            )
            self.open("https://www.whatsmyua.info/")
            user_agent_detected = self.get_text("#custom-ua-string")
            self._print("\nUser-Agent override = %s\n" % user_agent_detected)
            self.sleep(3)
        finally:
            # Reset the user-agent back to the original
            self.driver.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": original_user_agent},
            )
