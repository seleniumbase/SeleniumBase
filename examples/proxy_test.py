from seleniumbase.config import settings
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ProxyTests(BaseCase):
    def test_proxy(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            print("Skipping test in Headless Mode.")
            self.skip("Skipping test in Headless Mode.")
        elif self.recorder_mode:
            self.open_if_not_url("about:blank")
            print("Skipping test in Recorder Mode.")
            self.skip("Skipping test in Recorder Mode.")
        elif self.browser == "safari":
            self.open_if_not_url("about:blank")
            print("Skipping test for using Safari.")
            self.skip("Skipping test for using Safari.")
        settings.SKIP_JS_WAITS = True
        if not self.page_load_strategy == "none" and not self.undetectable:
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
