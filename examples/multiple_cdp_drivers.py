from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class MultipleDriversTest(BaseCase):
    def test_multiple_drivers(self):
        url1 = "https://seleniumbase.io/demo_page"
        self.activate_cdp_mode(url1)
        driver1 = self.driver
        url2 = "https://seleniumbase.io/coffee/"
        driver2 = self.get_new_driver(undetectable=True)
        self.activate_cdp_mode(url2)
        print("\n" + driver1.get_current_url())
        print(driver2.get_current_url())
