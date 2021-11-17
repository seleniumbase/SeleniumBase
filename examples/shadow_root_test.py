from seleniumbase import BaseCase


class ShadowRootTest(BaseCase):
    def test_shadow_root(self):
        self.open("https://react-shadow.herokuapp.com/Patagonia")
        self.click("section.weather::shadow div::shadow button")
        self.assert_element('section.weather::shadow img[alt="Patagonia"]')
        weather = self.get_text("section.weather::shadow h1")
        self.post_message(weather)
        self.click('section.weather::shadow a[href="/Kyoto"]')
        self.assert_element('section.weather::shadow img[alt="Kyoto"]')
        weather = self.get_text("section.weather::shadow h1")
        self.post_message(weather)
