from seleniumbase import BaseCase


class PdfAssertTests(BaseCase):
    def test_assert_pdf_text(self):
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
