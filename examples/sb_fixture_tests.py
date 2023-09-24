# "sb" pytest fixture test in a method with no class
def test_sb_fixture_with_no_class(sb):
    sb.open("seleniumbase.io/simple/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.click('a:contains("Sign in")')
    sb.assert_exact_text("Welcome!", "h1")
    sb.assert_element("img#image1")
    sb.highlight("#image1")
    sb.click_link("Sign out")
    sb.assert_text("signed out", "#top_message")


# "sb" pytest fixture test in a method inside a class
class Test_SB_Fixture:
    def test_sb_fixture_inside_class(self, sb):
        sb.open("seleniumbase.io/simple/login")
        sb.type("#username", "demo_user")
        sb.type("#password", "secret_pass")
        sb.click('a:contains("Sign in")')
        sb.assert_exact_text("Welcome!", "h1")
        sb.assert_element("img#image1")
        sb.highlight("#image1")
        sb.click_link("Sign out")
        sb.assert_text("signed out", "#top_message")
