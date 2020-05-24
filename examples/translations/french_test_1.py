# French Language Test
from seleniumbase.translate.french import CasDeBase


class MaClasseDeTest(CasDeBase):

    def test_exemple_1(self):
        self.ouvrir("https://fr.wikipedia.org/wiki/")
        self.vérifier_texte("Wikipédia")  # noqa
        self.vérifier_élément('[title="Visiter la page d’accueil"]')
        self.modifier_texte("#searchInput", "Crème brûlée")
        self.cliquez_sur("#searchButton")
        self.vérifier_texte("Crème brûlée", "#firstHeading")
        self.vérifier_élément('img[alt*="Crème brûlée"]')
        self.modifier_texte("#searchInput", "Jardin des Tuileries")
        self.cliquez_sur("#searchButton")
        self.vérifier_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_vrai("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_vrai("Jardin" in self.obtenir_url_actuelle())
