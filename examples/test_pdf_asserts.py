from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class PDFAssertTests(BaseCase):
    def test_assert_pdf_text(self):
        self.goto("data:,")
        if self.headless:
            self.skip("Skip this test in headless mode!")
        if not self.undetectable or not self.external_pdf:
            self.activate_cdp_mode(external_pdf=True)
        # Assert PDF contains the expected text on Page 1
        self.assert_pdf_text(
            "https://nostarch.com/download/Automate_the_Boring_Stuff_dTOC.pdf",
            "Programming Is a Creative Activity",
            page=1,
        )
        # Assert PDF contains the expected text on any of the pages
        self.assert_pdf_text(
            "https://nostarch.com/download/Automate_the_Boring_Stuff_dTOC.pdf",
            "Extracting Text from PDFs",
        )
