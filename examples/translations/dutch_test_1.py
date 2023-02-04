# Dutch Language Test
from seleniumbase.translate.dutch import Testgeval
Testgeval.main(__name__, __file__)


class MijnTestklasse(Testgeval):
    def test_voorbeeld_1(self):
        self.openen("https://nl.wikipedia.org/wiki/Hoofdpagina")
        self.controleren_element('a[title*="hoofdpagina gaan"]')
        self.controleren_tekst("Welkom op Wikipedia", "td.hp-welkom")
        self.typ("#searchInput", "Stroopwafel")
        self.klik("#searchButton")
        self.controleren_tekst("Stroopwafel", "#firstHeading")
        self.controleren_element('img[src*="Stroopwafels"]')
        self.typ("#searchInput", "Rijksmuseum Amsterdam")
        self.klik("#searchButton")
        self.controleren_tekst("Rijksmuseum", "#firstHeading")
        self.controleren_element('img[src*="Rijksmuseum"]')
        self.terug()
        self.controleren_url_bevat("Stroopwafel")
        self.vooruit()
        self.controleren_url_bevat("Rijksmuseum")
