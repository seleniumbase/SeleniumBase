from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--enable-3d-apis")


class ThreeJSTests(BaseCase):
    def test_animation(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            self.skip("Skip this test in headless mode!")
        if self.is_chromium() and not self.enable_3d_apis:
            self.get_new_driver(enable_3d_apis=True)  # --enable-3d-apis
        url = "https://threejs.org/examples/#webgl_animation_skinning_morph"
        self.open(url)
        self.switch_to_frame("iframe#viewer")
        self.sleep(0.8)
        self.click('button:contains("Wave")')
        self.sleep(3)
