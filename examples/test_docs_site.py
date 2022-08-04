from seleniumbase import BaseCase


class DocsSiteTests(BaseCase):
    def test_docs(self):
        self.open("https://seleniumbase.io/examples/ReadMe/")
        self.assert_exact_text("Running Example Tests", "h1")
        self.js_click('a[href="../../help_docs/customizing_test_runs/"]')
        self.assert_exact_text("Command Line Options", "h1")
        self.js_click('a[href="../../examples/example_logs/ReadMe/"]')
        self.assert_exact_text("Dashboard / Reports", "h1")
        self.js_click('a[href*="/seleniumbase/console_scripts/ReadMe/"]')
        self.assert_exact_text("Console Scripts", "h1")
        self.js_click('a[href="../../../help_docs/syntax_formats/"]')
        self.assert_exact_text("Syntax Formats", "h1")
        self.js_click('a[href="../recorder_mode/"]')
        self.assert_exact_text("Recorder Mode", "h1")
        self.js_click('a[href="../method_summary/"]')
        self.assert_exact_text("API Reference", "h1")
        self.click('img[alt="logo"]')
        self.assert_text("SeleniumBase", "h1")
