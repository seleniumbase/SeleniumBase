from test_framework.fixtures import base_case

class MyTestClass(base_case.BaseCase):

    def test_basic(self):
        self.driver.get("http://www.wikipedia.org/")
        self.wait_for_element_visible("a[href='//en.wikipedia.org/']", timeout=5).click()
        self.wait_for_element_visible("div#simpleSearch", timeout=5)
        self.wait_for_element_visible("input[name='search']", timeout=5)
        self.update_text_value("input[name='search']", "Boston\n")
        text = self.wait_for_element_visible("div#mw-content-text", timeout=5).text
        self.assertTrue("The Charles River separates Boston from " in text)
        self.wait_for_element_visible("a[title='Find out about Wikipedia']").click()
        self.wait_for_text_visible("Since its creation in 2001", "div#mw-content-text", timeout=5)

        self.driver.get("http://www.wikimedia.org/")
        self.wait_for_element_visible('img[alt="Wikivoyage"]', timeout=5).click()
        self.wait_for_element_visible("a[href='//en.wikivoyage.org/']", timeout=5).click()
        self.wait_for_element_visible('a[title="Visit the main page"]', timeout=5)
        self.wait_for_element_visible('input#searchInput', timeout=5)
        self.update_text_value("input#searchInput", "Israel\n")
        self.wait_for_element_visible("div#contentSub", timeout=5)
        text = self.wait_for_element_visible("div#mw-content-text", timeout=5).text
        self.assertTrue("The state of Israel" in text)
