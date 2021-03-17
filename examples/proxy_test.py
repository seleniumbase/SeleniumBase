import time
from seleniumbase import BaseCase


class ProxyTests(BaseCase):

    def test_proxy(self):
        self.open('https://ipinfo.io/')
        ip_address = self.get_text("div.home-ip-details span.value")[1:-1]
        print("\n\nMy IP Address = %s\n" % ip_address)
        print("Displaying Host Info:")
        text = self.get_text('div.home-ip-details').split('asn:')[0]
        rows = text.split('\n')
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', ' '))
        print("\nThe browser will close automatically in 7 seconds...")
        time.sleep(7)
