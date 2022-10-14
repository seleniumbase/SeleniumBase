from seleniumbase import BaseCase


class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
        self.assert_text("Welcome!", "h1")
        self.highlight("img#image1")  # A fancier assert_element() call
        self.click('a:contains("This Page")')  # Use :contains() on any tag
        self.save_screenshot_to_logs()  # In "./latest_logs/" folder.
        self.click_link("Sign out")  # Link must be "a" tag. Not "button".
        self.assert_element('a:contains("Sign in")')
        self.assert_exact_text("You have been signed out!", "#top_message")
