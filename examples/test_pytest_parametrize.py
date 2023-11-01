import pytest


@pytest.mark.parametrize(
    "value", ["List of Features", "Command Line Options"]
)
def test_sb_fixture_with_no_class(sb, value):
    sb.open("seleniumbase.io/help_docs/install/")
    sb.type('input[aria-label="Search"]', value)
    sb.click("nav h1 mark")
    sb.assert_title_contains(value)
    sb.assert_text(value, "div.md-content")


class Test_SB_Fixture:
    @pytest.mark.parametrize(
        "value", ["Console Scripts", "API Reference"]
    )
    def test_sb_fixture_inside_class(self, sb, value):
        sb.open("seleniumbase.io/help_docs/install/")
        sb.type('input[aria-label="Search"]', value)
        sb.click("nav h1 mark")
        sb.assert_title_contains(value)
        sb.assert_text(value, "div.md-content")
