from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class HandleAlertTests(BaseCase):
    def test_alerts(self):
        self.open("about:blank")
        self.execute_script('window.alert("ALERT!!!");')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        self.accept_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
        self.execute_script('window.prompt("My Prompt","defaultText");')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        alert = self.switch_to_alert()
        self.assert_equal(alert.text, "My Prompt")  # Not input field
        self.dismiss_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
