# Spanish Language Test
from seleniumbase.translate.spanish import CasoDePrueba
CasoDePrueba.main(__name__, __file__)


class MiClaseDePrueba(CasoDePrueba):
    def test_ejemplo_1(self):
        self.abrir("https://es.wikipedia.org/wiki/")
        self.verificar_texto("Wikipedia")
        self.verificar_elemento('[title="Wikipedia:Bienvenidos"]')
        self.escriba('[name="search"]', "Parque de Atracciones Tibidabo")
        self.haga_clic('button:contains("Buscar")')
        self.verificar_texto("Tibidabo", "#firstHeading")
        self.verificar_elemento('img[alt*="Tibidabo"]')
        self.escriba('input[name="search"]', "Palma de Mallorca")
        self.haga_clic('button:contains("Buscar")')
        self.verificar_texto("Palma de Mallorca", "#firstHeading")
        self.verificar_elemento('img[alt*="Palma"]')
        self.volver()
        self.verificar_url_contiene("Tibidabo")
        self.adelante()
        self.verificar_url_contiene("Mallorca")
