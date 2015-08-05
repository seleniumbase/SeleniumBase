""" test_fail.py """
from seleniumbase.fixtures import base_case

class MyTestClass(base_case.BaseCase):

    def test_find_google_on_bing(self):
        self.driver.get("http://bing.com")
        self.wait_for_element_visible("div#google_is_here", timeout=3)
