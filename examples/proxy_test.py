from seleniumbase.config import settings
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ProxyTests(BaseCase):
    def test_proxy(self):
        if self.headless or self.recorder_mode or self.browser == "safari":
            self.open_if_not_url("about:blank")
            print("\n  Unsupported mode for this test.")
            self.skip("Unsupported mode for this test.")
        settings.SKIP_JS_WAITS = True
        self.open("https://api.ipify.org/")
        ip_address = self.get_text("body")
        if "ERR" in ip_address:
            raise Exception("Failed to determine IP Address!")
        print("\n\nMy IP Address = %s\n" % ip_address)
        self.open("https://ipinfo.io/%s" % ip_address)
        self.sleep(2)
        self.wait_for_text(ip_address, "h1", timeout=20)
        self.wait_for_element_present('[href="/signup"]')
        self.wait_for_text("Hosted domains", timeout=20)
        self.highlight("h1")
        pop_up = '[role="dialog"] span.cursor-pointer'
        self.click_if_visible(pop_up)
        self.highlight("#block-summary")
        self.click_if_visible(pop_up)
        self.highlight("#block-geolocation")
        self.click_if_visible(pop_up)
        self.sleep(2)
        print("Displaying Host Info:")
        text = self.get_text("#block-summary").split("Hosted domains")[0]
        rows = text.split("\n")
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', ' "'))
        print("\nDisplaying GeoLocation Info:")
        text = self.get_text("#block-geolocation")
        text = text.split("IP Geolocation data")[0]
        rows = text.split("\n")
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', ' "'))
        self.click_if_visible(pop_up)
        self.sleep(3)
