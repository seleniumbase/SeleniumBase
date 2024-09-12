from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class TestGeolocation(BaseCase):
    def tearDown(self):
        self.save_teardown_screenshot()  # If test fails, or if "--screenshot"
        if self.is_chromium() and not self._multithreaded:
            # Reset Permissions and GeolocationOverride
            try:
                self.open("about:blank")
                self.execute_cdp_cmd("Emulation.setGeolocationOverride", {})
                self.execute_cdp_cmd("Browser.resetPermissions", {})
            except Exception:
                pass
        super().tearDown()

    def test_geolocation(self):
        self.open("about:blank")
        if self._multithreaded:
            self.skip("Skipping test in multi-threaded mode.")
        if not self.is_chromium():
            print("\n* execute_cdp_cmd() is only for Chromium browsers")
            self.skip("execute_cdp_cmd() is only for Chromium browsers")
        self.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": "https://www.openstreetmap.org/",
                "permissions": ["geolocation"],
            },
        )
        self.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",
            {
                "latitude": 48.87645,
                "longitude": 2.26340,
                "accuracy": 100,
            },
        )
        self.open("https://www.openstreetmap.org/")
        self.click("span.geolocate")
        self.assert_url_contains("48.876450/2.263400")
        self.save_screenshot_to_logs()
        if self.headed:
            self.sleep(4)
