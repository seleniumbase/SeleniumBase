import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


@pytest.mark.offline  # Can be run with: "pytest -m offline"
class OfflineTests(BaseCase):
    def test_get_user_agent(self):
        self.open("data:,")
        user_agent = self.get_user_agent()
        print('\nUser Agent = "%s"' % user_agent)

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
            new_user_agent = self.get_user_agent()
            print('\nOverrided User Agent = "%s"' % new_user_agent)
        finally:
            # Reset the user-agent back to the original
            self.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {"userAgent": user_agent},
            )
        print("\n--------------------------")
        user_agent = self.get_user_agent()
        print('\nUser Agent = "%s"' % user_agent)
