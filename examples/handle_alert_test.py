from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_alerts(self):
        self.open("about:blank")
        self.execute_script('window.alert("ALERT!!!")')
        self.sleep(1.2)  # Not needed (Lets you see the alert pop up)
        self.wait_for_and_accept_alert()
        self.sleep(0.8)  # Not needed (Lets you see the alert go away)
        self.execute_script('window.prompt("My Prompt","defaultText");')
        self.sleep(1.2)  # Not needed (Lets you see the alert pop up)
        alert = self.wait_for_and_switch_to_alert(timeout=2)
        self.assert_equal(alert.text, "My Prompt")  # Not the input field
        self.wait_for_and_dismiss_alert()
        self.sleep(0.8)  # Not needed (Lets you see the alert go away)
