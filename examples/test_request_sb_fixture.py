# Use the pytest "request" fixture to get the "sb" fixture (no class)
def test_request_sb_fixture(request):
    sb = request.getfixturevalue("sb")
    sb.open("https://seleniumbase.io/demo_page")
    sb.assert_text("SeleniumBase", "#myForm h2")
    sb.assert_element("input#myTextInput")
    sb.type("#myTextarea", "This is me")
    sb.click("#myButton")
    sb.tearDown()


# Use the pytest "request" fixture to get the "sb" fixture (in class)
class Test_Request_Fixture:
    def test_request_sb_fixture_in_class(self, request):
        sb = request.getfixturevalue("sb")
        sb.open("https://seleniumbase.io/demo_page")
        sb.assert_element("input#myTextInput")
        sb.type("#myTextarea", "Automated")
        sb.assert_text("This Text is Green", "#pText")
        sb.click("#myButton")
        sb.assert_text("This Text is Purple", "#pText")
        sb.tearDown()
