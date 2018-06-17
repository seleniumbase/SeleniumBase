import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_proxy(self):
        self.open('https://ipinfo.io/')
        ip_address = self.get_text("div.home-ip-details span.value")[1:-1]
        self.open('https://ipinfo.io/%s' % ip_address)
        print("\n\nIP Address = %s\n" % ip_address)
        print("Displaying Host Info:")
        print(self.get_text('table.table'))
        print("\nThe browser will close automatically in 7 seconds...")
        time.sleep(7)
