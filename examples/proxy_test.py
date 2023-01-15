from seleniumbase.config import settings
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ProxyTests(BaseCase):
    def test_proxy(self):
        settings.SKIP_JS_WAITS = True
        if not self.page_load_strategy == "none":
            # This page takes too long to load otherwise
            self.get_new_driver(page_load_strategy="none")
        self.open("https://ipinfo.io/")
        ip_address = self.get_text('#ip-string span[class*="primary"] span')
        print("\n\nMy IP Address = %s\n" % ip_address)
        print("Displaying Host Info:")
        text = self.get_text("#widget-scrollable-container").split("asn:")[0]
        rows = text.split("\n")
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', " "))
        if not self.headless:
            print("\nThe browser will close automatically in 7 seconds...")
            self.sleep(7)
