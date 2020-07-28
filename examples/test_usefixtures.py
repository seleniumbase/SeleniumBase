import pytest


@pytest.mark.usefixtures("sb")
class Test_UseFixtures():
    def test_usefixtures_on_class(self):
        sb = self.sb
        sb.open("https://google.com/ncr")
        sb.update_text('input[title="Search"]', 'SeleniumBase\n')
        sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
        sb.assert_text("SeleniumBase", 'strong[itemprop="name"]')
        sb.assert_text("integrations")
        sb.assert_element('a[title="help_docs"]')
        sb.click('a[title="examples"]')
