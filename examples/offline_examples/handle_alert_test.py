import pytest
from seleniumbase import BaseCase


@pytest.mark.offline  # Can be run with: "pytest -m offline"
class OfflineTestClass(BaseCase):

    def test_alerts(self):
        self.open("data:,")
        self.execute_script('window.alert("ALERT!!!")')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        self.accept_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
        self.execute_script('window.prompt("My Prompt","defaultText");')
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        alert = self.switch_to_alert()
        self.assert_equal(alert.text, "My Prompt")  # Not input field
        self.dismiss_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
