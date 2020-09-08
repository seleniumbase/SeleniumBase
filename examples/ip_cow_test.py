import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_ip_cow(self):
        self.open('https://www.ipcow.com/')
        ip_data = self.get_text("table tbody")
        print("\n\n*** IP and Browser Data: ***")
        print(ip_data)
        print("\nThe browser will close automatically in 7 seconds...")
        time.sleep(7)
