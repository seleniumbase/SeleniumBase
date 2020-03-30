# Portuguese Language Test - Python 3 Only!
from seleniumbase.translate.portuguese import CasoDeTeste


class MinhaClasseDeTeste(CasoDeTeste):

    def test_exemplo_1(self):
        self.abrir_url("https://pt.wikipedia.org/wiki/")
        self.verificar_texto("Wikipédia")
        self.verificar_elemento('[title="Visitar a página principal"]')
        self.atualizar_texto("#searchInput", "Rio de Janeiro")
        self.clique("#searchButton")
        self.verificar_texto("Rio de Janeiro", "#firstHeading")
        self.verificar_elemento('img[alt*="edifícios"]')
        self.atualizar_texto("#searchInput", "São Paulo")
        self.clique("#searchButton")
        self.verificar_texto("São Paulo", "#firstHeading")
        self.verificar_elemento('img[src*="Monumento"]')
        self.voltar()
        self.verificar_verdade("Janeiro" in self.obter_url_atual())
        self.avançar()  # noqa
        self.verificar_verdade("Paulo" in self.obter_url_atual())
