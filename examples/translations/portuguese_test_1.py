# Portuguese Language Test
from seleniumbase.translate.portuguese import CasoDeTeste


class MinhaClasseDeTeste(CasoDeTeste):
    def test_exemplo_1(self):
        self.abrir("https://pt.wikipedia.org/wiki/")
        self.verificar_texto("Wikipédia")
        self.verificar_elemento('[title="Língua portuguesa"]')
        self.digitar("#searchform input", "João Pessoa")
        self.clique("#searchform button")
        self.verificar_texto("João Pessoa", "#firstHeading")
        self.verificar_elemento('img[alt*="João Pessoa"]')
        self.digitar("#searchform input", "Florianópolis")
        self.clique("#searchform button")
        self.verificar_texto("Florianópolis", "h1#firstHeading")
        self.verificar_elemento('td:contains("Avenida Beira-Mar")')
        self.voltar()
        self.verificar_verdade("João" in self.obter_url_atual())
        self.atualizar_a_página()  # noqa
        self.digitar("#searchform input", "Teatro Amazonas")
        self.clique("#searchform button")
        self.verificar_texto("Teatro Amazonas", "#firstHeading")
        self.verificar_texto_do_link("Festival Amazonas de Ópera")
