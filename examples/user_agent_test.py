from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_user_agent(self):
        self.open('https://www.whatsmyua.info/')
        user_agent = self.get_text("#custom-ua-string")
        print("\n\nUser-Agent = %s\n" % user_agent)
        print("Displaying User-Agent Info:")
        print(self.get_text("#useragent"))
        print("\nThe browser will close automatically in 7 seconds...")
        self.sleep(7)
