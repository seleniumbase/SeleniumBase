import pytest


# Use the pytest "request" fixture to get the "sb" fixture (no class)
@pytest.mark.offline
def test_request_fixture(request):
    sb = request.getfixturevalue("sb")
    sb.open("data:text/html,<p>Hello<br><input></p>")
    sb.assert_element("html > body")
    sb.assert_text("Hello", "body p")
    sb.type("input", "Goodbye")
    sb.click("body p")
    sb.tearDown()


# Use the pytest "request" fixture to get the "sb" fixture (in class)
@pytest.mark.offline
class RequestTests:
    def test_request_fixture_in_class(self, request):
        sb = request.getfixturevalue("sb")
        sb.open("data:text/html,<p>Hello<br><input></p>")
        sb.assert_element("html > body")
        sb.assert_text("Hello", "body p")
        sb.type("input", "Goodbye")
        sb.click("body p")
        sb.tearDown()
