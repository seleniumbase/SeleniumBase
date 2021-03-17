# French Language Test
from seleniumbase.translate.french import CasDeBase


class MaClasseDeTest(CasDeBase):

    def test_exemple_1(self):
        self.ouvrir("https://fr.wikipedia.org/wiki/")
        self.vérifier_texte("Wikipédia")  # noqa
        self.vérifier_élément('[alt="Wikipédia"]')
        self.js_taper("#searchform input", "Crème brûlée")
        self.cliquer("#searchform button")
        self.vérifier_texte("Crème brûlée", "#firstHeading")
        self.vérifier_élément('img[alt*="Crème brûlée"]')
        self.taper("#searchform input", "Jardin des Tuileries")
        self.cliquer("#searchform button")
        self.vérifier_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_vrai("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_vrai("Jardin" in self.obtenir_url_actuelle())
