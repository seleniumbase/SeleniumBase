# French / Français - Translations - Python 3 Only!
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class CasDeBase(BaseCase):

    def __init__(self, *args, **kwargs):
        super(CasDeBase, self).__init__(*args, **kwargs)
        self._language = "French"

    def ouvrir(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def ouvrir_url(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def cliquer(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def double_cliquer(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def cliquer_lentement(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def cliquer_si_affiché(self, *args, **kwargs):  # noqa
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def cliquer_texte_du_lien(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def modifier_texte(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def taper(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def ajouter_texte(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def obtenir_texte(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def vérifier_texte(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def vérifier_texte_exactement(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def vérifier_texte_du_lien(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def vérifier_élément(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def vérifier_élément_affiché(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def vérifier_élément_pas_affiché(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def vérifier_élément_présent(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def vérifier_élément_pas_présent(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def vérifier_titre(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def obtenir_titre(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def vérifier_vrai(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def vérifier_faux(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def vérifier_égal(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def vérifier_non_égal(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def rafraîchir_la_page(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def obtenir_url_actuelle(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def obtenir_html_de_la_page(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def retour(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def en_avant(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def est_texte_affiché(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def est_un_élément_affiché(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def est_un_élément_activé(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def est_un_élément_présent(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def attendre_le_texte(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def attendre_un_élément(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def attendre_un_élément_affiché(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def attendre_un_élément_pas_affiché(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def attendre_un_élément_présent(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def attendre_un_élément_pas_présent(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def dormir(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def attendre(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def soumettre(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def effacer(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def concentrer(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def js_cliquer(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def js_modifier_texte(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def js_taper(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def vérifier_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def enregistrer_capture_d_écran(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def sélectionner_fichier(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def exécuter_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def exécuter_script_sans_risque(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def activer_jquery(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def annonces_de_bloc(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def sauter(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def vérifier_les_liens_rompus(self, *args, **kwargs):
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

    def passer_à_fenêtre(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def passer_à_fenêtre_par_défaut(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def passer_à_fenêtre_dernière(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def maximiser_fenêtre(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

    def illuminer(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def illuminer_cliquer(self, *args, **kwargs):
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

    def planer_au_dessus_et_cliquer(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def est_il_sélectionné(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def appuyer_sur_flèche_haut(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def appuyer_sur_flèche_bas(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def appuyer_sur_flèche_gauche(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def appuyer_sur_flèche_droite(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def cliquer_éléments_visibles(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def sélectionner_option_par_texte(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def sélectionner_option_par_index(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def sélectionner_option_par_valeur(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def créer_une_présentation(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def ajouter_une_diapositive(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def enregistrer_la_présentation(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def démarrer_la_présentation(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def créer_un_graphique_à_secteurs(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def créer_un_graphique_à_barres(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def créer_un_graphique_à_colonnes(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def créer_un_graphique_linéaire(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def créer_un_graphique_en_aires(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def ajouter_séries_au_graphique(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def ajouter_un_point_de_données(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def enregistrer_le_graphique(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def afficher_le_graphique(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def extraire_le_graphique(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def créer_une_visite(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def créer_une_visite_shepherd(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def créer_une_visite_bootstrap(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def créer_une_visite_driverjs(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def créer_une_visite_hopscotch(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def créer_une_visite_introjs(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def ajouter_étape_à_la_visite(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def jouer_la_visite(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def exporter_la_visite(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def obtenir_texte_pdf(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def vérifier_texte_pdf(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def vérifier_fichier_téléchargé(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def échouer(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def obtenir(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def visiter(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def visiter_url(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def obtenir_élément(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def trouver_élément(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def supprimer_élément(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def supprimer_éléments(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def trouver_texte(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def définir_texte(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def obtenir_attribut(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def définir_attribut(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def définir_attributs(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def écriver(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def définir_thème_du_message(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def afficher_message(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def imprimer(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def reporté_vérifier_élément(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def reporté_vérifier_texte(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def effectuer_vérifications_reportées(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def accepter_alerte(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def rejeter_alerte(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def passer_à_alerte(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def glisser_et_déposer(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def définir_html(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def charger_html_fichier(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def ouvrir_html_fichier(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def supprimer_tous_les_cookies(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def obtenir_agent_utilisateur(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def obtenir_code_de_langue(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_Français(MasterQA, CasDeBase):

    def vérifier(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Vérification manuelle"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "La page est-elle bonne?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
