import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_get_ip_address_with_bing(self):
        self.open('https://www.bing.com/search?q=what+is+my+ip')
        ip_address = self.get_text("#b_results li.b_top")
        print("\n\n%s\n" % ip_address)
        print("\nThe browser will close automatically in 7 seconds...")
        time.sleep(7)
