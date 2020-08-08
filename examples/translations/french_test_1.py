# French Language Test
from seleniumbase.translate.french import CasDeBase


class MaClasseDeTest(CasDeBase):

    def test_exemple_1(self):
        self.ouvrir("https://fr.wikipedia.org/wiki/")
        self.vérifier_texte("Wikipédia")  # noqa
        self.vérifier_élément('[alt="Wikipédia"]')
        self.taper("#searchInput", "Crème brûlée")
        self.cliquer("#searchButton")
        self.vérifier_texte("Crème brûlée", "#firstHeading")
        self.vérifier_élément('img[alt*="Crème brûlée"]')
        self.taper("#searchInput", "Jardin des Tuileries")
        self.cliquer("#searchButton")
        self.vérifier_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_vrai("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_vrai("Jardin" in self.obtenir_url_actuelle())
