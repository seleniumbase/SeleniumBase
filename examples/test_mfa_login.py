from seleniumbase import BaseCase


class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")
        self.highlight("img#image1")
        self.assert_text("Welcome!", "h1")
        self.save_screenshot_to_logs()
