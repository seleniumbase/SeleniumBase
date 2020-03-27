# Italian Language Test
from seleniumbase.translate.italian import CasoDiProva


class ClasseDiTest(CasoDiProva):

    def test_esempio_1(self):
        self.apri_url("https://it.wikipedia.org/wiki/")
        self.verificare_il_testo("Wikipedia")
        self.verificare_elemento('[title="Lingua italiana"]')
        self.aggiornare_il_testo("#searchInput", "Pizza")
        self.fare_clic("#searchButton")
        self.verificare_il_testo("Pizza", "#firstHeading")
        self.verificare_elemento('img[alt*="pizza"]')
        self.aggiornare_il_testo("#searchInput", "Colosseo")
        self.fare_clic("#searchButton")
        self.verificare_il_testo("Colosseo", "#firstHeading")
        self.verificare_elemento('img[alt*="Colosseo"]')
        self.indietro()
        self.verificare_correttezza("Pizza" in self.ottenere_url_corrente())
        self.avanti()
        self.verificare_correttezza("Colosseo" in self.ottenere_url_corrente())
