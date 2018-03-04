import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_proxy(self):
        self.open('https://ipinfo.io/')
        ip_address = self.get_page_title().split(' ')[0]
        print("\n\nIP Address = %s\n" % ip_address)
        href = '/%s' % ip_address
        self.click('[href="%s"]' % href)
        print("Displaying Host Info:")
        print(self.get_text('table.table'))
        print("\nThe browser will close automatically in 7 seconds...")
        time.sleep(7)
