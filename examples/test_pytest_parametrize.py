import pytest


@pytest.mark.parametrize("value", ["pytest", "selenium"])
def test_sb_fixture_with_no_class(sb, value):
    sb.open("https://duckduckgo.com/")
    sb.type('input[name="q"]', value + "\n")
    sb.assert_text(value, "div.results")


class Test_SB_Fixture:
    @pytest.mark.parametrize("value", ["pytest", "selenium"])
    def test_sb_fixture_inside_class(self, sb, value):
        sb.open("https://duckduckgo.com/")
        sb.type('input[name="q"]', value + "\n")
        sb.assert_text(value, "div.results")
