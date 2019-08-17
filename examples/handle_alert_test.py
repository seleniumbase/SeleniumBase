import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_alerts(self):
        self.open("about:blank")
        self.execute_script('window.alert("ALERT!!!")')
        time.sleep(1.2)  # Not needed (Lets you see the alert pop up)
        self.wait_for_and_accept_alert()
        time.sleep(0.8)  # Not needed (Lets you see the alert go away)
