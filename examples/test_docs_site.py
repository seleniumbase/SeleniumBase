from seleniumbase import BaseCase


class DocsSiteTests(BaseCase):
    def test_docs(self):
        self.open("https://seleniumbase.io/")
        self.assert_exact_text("SeleniumBase ReadMe", "h1")
        self.click('a[href="help_docs/features_list/"]')
        self.assert_exact_text("Features List", "h1")
        self.click('a[href="../../examples/ReadMe/"]')
        self.assert_exact_text("Running Example Tests", "h1")
        self.click('a[href="../../help_docs/customizing_test_runs/"]')
        self.assert_exact_text("Command Line Options", "h1")
        self.click('a[href="../../examples/example_logs/ReadMe/"]')
        self.assert_exact_text("Dashboard / Reports", "h1")
        self.click('a[href="../../../seleniumbase/console_scripts/ReadMe/"]')
        self.assert_exact_text("Console Scripts", "h1")
        self.click('a[href="../../../help_docs/syntax_formats/"]')
        self.assert_exact_text("Syntax Formats", "h1")
        self.click('a[href="../recorder_mode/"]')
        self.assert_exact_text("Recorder Mode", "h1")
        self.click('a[href="../method_summary/"]')
        self.assert_exact_text("API Reference", "h1")
        self.click('img[alt="logo"]')
        self.assert_exact_text("SeleniumBase ReadMe", "h1")
