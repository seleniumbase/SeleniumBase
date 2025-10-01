from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


# "sb" pytest fixture test in a method with no class
def test_sb_fixture_with_no_class(sb: BaseCase):
    sb.open("seleniumbase.io/help_docs/install/")
    sb.type('input[aria-label="Search"]', "GUI Commander")
    sb.click('mark:contains("Commander")')
    sb.assert_title_contains("GUI / Commander")


# "sb" pytest fixture test in a method inside a class
class Test_SB_Fixture:
    def test_sb_fixture_inside_class(self, sb: BaseCase):
        sb.open("seleniumbase.io/help_docs/install/")
        sb.type('input[aria-label="Search"]', "GUI Commander")
        sb.click('mark:contains("Commander")')
        sb.assert_title_contains("GUI / Commander")
