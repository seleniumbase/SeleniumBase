from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class UserAgentTests(BaseCase):
    def test_user_agent(self):
        self.open("data:text/html,<h1></h1>")
        user_agent_detected = self.get_user_agent()
        self.set_text_content("h1", user_agent_detected)
        self.highlight("h1")
        original_user_agent = user_agent_detected
        if not self.user_agent:
            # Using the built-in user-agent string
            print("\n\nUser-Agent: %s" % user_agent_detected)
        else:
            # User-agent was overridden using: --agent=STRING
            print("\n\nUser-Agent override: %s" % user_agent_detected)
        if self.headed:
            self.sleep(2.75)

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
            self.open("about:blank")
            self.sleep(0.1)  # Enough to see that page was refreshed
            self.open("data:text/html,<h1></h1>")
            user_agent_detected = self.get_user_agent()
            self.set_text_content("h1", user_agent_detected)
            self.highlight("h1")
            print("\nUser-Agent override: %s" % user_agent_detected)
            if self.headed:
                self.sleep(2.75)
        finally:
            # Reset the user-agent back to the original
            self.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": original_user_agent},
            )
