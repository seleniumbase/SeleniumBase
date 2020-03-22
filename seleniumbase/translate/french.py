# French Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class CasDeBase(BaseCase):

    def ouvrir_url(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def cliquez_sur(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def double_clic(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def cliquez_lentement(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def cliquez_sur_le_texte_du_lien(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def modifier_le_texte(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def ajouter_du_texte(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def obtenir_du_texte(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def vérifier_le_texte(self, *args, **kwargs):  # noqa
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def vérifier_exactement_le_texte(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def vérifier_un_élément(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def vérifier_le_titre(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def vérifier_la_vérité(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def vérifier_le_mensonge(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def vérifier_la_véracité(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def vérifier_la_fausseté(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def rafraîchir_la_page(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def obtenir_url_actuelle(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def obtenir_le_html_de_la_page(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def retour(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def en_avant(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def est_le_texte_affiché(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def est_un_élément_affiché(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def est_un_élément_présent(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def attendez_le_texte(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def attendre_un_élément(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def dormir(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def soumettre(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def js_clic(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def vérifier_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def enregistrer_la_capture_d_écran(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def sélectionnez_un_fichier(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def exécutez_le_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def bloc_d_annonces(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def sauter(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def vérifiez_les_liens_rompus(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def vérifier_les_erreurs_js(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def passer_au_cadre(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def passer_au_contenu_par_défaut(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def ouvrir_une_nouvelle_fenêtre(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def passer_à_la_fenêtre(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def passer_à_la_fenêtre_par_défaut(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def mettez_en_surbrillance(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def mettez_en_surbrillance_et_cliquez(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def déménager_à(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def faites_défiler_vers_le_haut(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def faites_défiler_vers_le_bas(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)
