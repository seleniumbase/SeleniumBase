import pytest


@pytest.mark.offline
def test_request_fixture(request):
    sb = request.getfixturevalue('sb')
    sb.open("data:text/html,<p>Hello<br><input></p>")
    sb.assert_element("html > body")
    sb.assert_text("Hello", "body p")
    sb.type("input", "Goodbye")
    sb.click("body p")
    sb.tearDown()
