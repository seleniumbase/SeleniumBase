from seleniumbase import BaseCase


class UserAgentTests(BaseCase):

    def test_user_agent(self):
        self.open('http://whatsmyuseragent.org/')
        user_agent = self.get_text(".user-agent p")
        print("\n\nUser-Agent:\n%s\n" % user_agent)
        print(self.get_text(".ip-address p"))
        print("\nThe browser will close automatically in 7 seconds...")
        self.sleep(7)
