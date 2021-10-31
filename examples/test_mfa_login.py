from seleniumbase import BaseCase


class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        totp_code = self.get_totp_code("GAXG2MTEOR3DMMDG")
        self.type("#totpcode", totp_code)
        self.click("#log-in")
        self.highlight("img#image1")
        self.assert_text("Welcome!", "h1")
        self.save_screenshot_to_logs()
