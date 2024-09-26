from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class HandleAlertTests(BaseCase):
    def test_alerts(self):
        self.open("about:blank")
        self.execute_script('window.alert("ALERT!!!");')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        self.assert_true(self.is_alert_present())
        self.accept_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
        self.execute_script('window.prompt("My Prompt","defaultText");')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        alert = self.switch_to_alert()
        self.assert_equal(alert.text, "My Prompt")  # Not input field
        self.dismiss_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
        self.assert_false(self.is_alert_present())
        if self.browser == "safari" and self._reuse_session:
            # Alerts can freeze Safari if reusing the browser session
            self.driver.quit()
