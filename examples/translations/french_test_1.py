# French Language Test - Python 3 Only!
from seleniumbase.translate.french import CasDeBase


class ClasseDeTest(CasDeBase):

    def test_exemple_1(self):
        self.ouvrir_url("https://fr.wikipedia.org/wiki/")
        self.vérifier_le_texte("Wikipédia")  # noqa
        self.vérifier_un_élément('[title="Visiter la page d’accueil"]')
        self.modifier_le_texte("#searchInput", "Crème brûlée")
        self.cliquez_sur("#searchButton")
        self.vérifier_le_texte("Crème brûlée", "#firstHeading")
        self.vérifier_un_élément('img[alt*="Crème brûlée"]')
        self.modifier_le_texte("#searchInput", "Jardin des Tuileries")
        self.cliquez_sur("#searchButton")
        self.vérifier_le_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_un_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_la_vérité("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_la_vérité("Jardin" in self.obtenir_url_actuelle())
