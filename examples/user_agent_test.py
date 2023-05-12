from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class UserAgentTests(BaseCase):
    def test_user_agent(self):
        if self._multithreaded:
            self.open_if_not_url("about:blank")
            self.skip("Skipping test in multi-threaded mode.")
        self.open("https://my-user-agent.com/")
        zoom_in = "#ua_string{zoom: 1.8;-moz-transform: scale(1.8);}"
        self.add_css_style(zoom_in)
        self.highlight("#ua_string")
        user_agent_detected = self.get_text("#ua_string")
        original_user_agent = user_agent_detected
        if not self.user_agent:
            # Using the built-in user-agent string
            print("\n\nUser-Agent: %s" % user_agent_detected)
        else:
            # User-agent was overridden using: --agent=STRING
            print("\n\nUser-Agent override: %s" % user_agent_detected)
        if not (self.headless or self.headless2 or self.xvfb):
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
            self.sleep(0.05)  # Enough to see that the page was refreshed
            self.open("https://my-user-agent.com/")
            zoom_in = "#ua_string{zoom: 1.8;-moz-transform: scale(1.8);}"
            self.add_css_style(zoom_in)
            self.highlight("#ua_string")
            user_agent_detected = self.get_text("#ua_string")
            print("\nUser-Agent override: %s" % user_agent_detected)
            if not (self.headless or self.headless2 or self.xvfb):
                self.sleep(2.75)
        finally:
            # Reset the user-agent back to the original
            self.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": original_user_agent},
            )
