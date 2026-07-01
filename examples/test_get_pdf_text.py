from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class PDFTests(BaseCase):
    def test_get_pdf_text(self):
        self.goto("data:,")
        if self.headless:
            self.skip("Skip this test in headless mode!")
        if not self.undetectable or not self.external_pdf:
            self.activate_cdp_mode(external_pdf=True)
        pdf = (
            "https://nostarch.com/download/"
            "Automate_the_Boring_Stuff_sample_ch17.pdf"
        )
        pdf_text = self.get_pdf_text(pdf, page=1, nav=True)
        print("\n" + pdf_text)
