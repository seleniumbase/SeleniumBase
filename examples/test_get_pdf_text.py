from seleniumbase import BaseCase


class PdfTests(BaseCase):
    def test_get_pdf_text(self):
        pdf = (
            "https://nostarch.com/download/"
            "Automate_the_Boring_Stuff_sample_ch17.pdf"
        )
        pdf_text = self.get_pdf_text(pdf, page=1)
        self._print("\n" + pdf_text)
