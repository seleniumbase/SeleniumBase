# Portuguese Language Test - Python 3 Only!
from seleniumbase.translate.portuguese import CasoDeTeste


class MinhaClasseDeTeste(CasoDeTeste):

    def test_exemplo_1(self):
        self.abrir_url("https://pt.wikipedia.org/wiki/")
        self.verificar_texto("Wikipédia")
        self.verificar_elemento('[title="Língua portuguesa"]')
        self.atualizar_texto("#searchInput", "Rio de Janeiro")
        self.clique("#searchButton")
        self.verificar_texto("Rio de Janeiro", "#firstHeading")
        self.verificar_elemento('img[alt*="edifícios"]')
        self.atualizar_texto("#searchInput", "São Paulo")
        self.clique("#searchButton")
        self.verificar_texto("São Paulo", "h1#firstHeading")
        self.verificar_elemento('img[src*="Monumento"]')
        self.voltar()
        self.verificar_verdade("Rio" in self.obter_url_atual())
        self.atualizar_texto("#searchInput", "Florianópolis\n")
        self.verificar_texto("Florianópolis", "h1#firstHeading")
        self.verificar_elemento('img[alt*="Avenida Beira Mar"]')
