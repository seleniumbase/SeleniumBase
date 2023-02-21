# Italian Language Test
from seleniumbase.translate.italian import CasoDiProva
CasoDiProva.main(__name__, __file__)


class MiaClasseDiTest(CasoDiProva):
    def test_esempio_1(self):
        self.apri("https://it.wikipedia.org/wiki/")
        self.verificare_testo("Wikipedia")
        self.verificare_elemento('a[title="Lingua italiana"]')
        self.digitare("#searchInput", "Pizza")
        self.fare_clic("#searchButton")
        self.verificare_testo("Pizza", "#firstHeading")
        self.verificare_elemento('figure img[src*="pizza"]')
        self.digitare("#searchInput", "Colosseo")
        self.fare_clic("#searchButton")
        self.verificare_testo("Colosseo", "#firstHeading")
        self.verificare_elemento('figure img[src*="Colosseo"]')
        self.indietro()
        self.verificare_url_contiene("Pizza")
        self.avanti()
        self.verificare_url_contiene("Colosseo")
