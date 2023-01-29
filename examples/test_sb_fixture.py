# "sb" pytest fixture test in a method with no class
def test_sb_fixture_with_no_class(sb):
    sb.open("https://google.com/ncr")
    sb.remove_elements("iframe")
    sb.type('input[title="Search"]', "SeleniumBase GitHub\n")
    sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
    sb.click('a[title="seleniumbase"]')


# "sb" pytest fixture test in a method inside a class
class Test_SB_Fixture:
    def test_sb_fixture_inside_class(self, sb):
        sb.open("https://google.com/ncr")
        sb.remove_elements("iframe")
        sb.type('input[title="Search"]', "SeleniumBase GitHub\n")
        sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
        sb.click('a[title="seleniumbase"]')
