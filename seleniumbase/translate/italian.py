# Italian / Italiano - Translations - Python 3 Only!
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class CasoDiProva(BaseCase):

    def apri_url(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def fare_clic(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def doppio_clic(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def clicca_lentamente(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def fare_clic_sul_testo_del_collegamento(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def aggiornare_il_testo(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def aggiungi_testo(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def ottenere_il_testo(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def verificare_il_testo(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def verificare_il_testo_esatto(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def verificare_testo_del_collegamento(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def verificare_elemento(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def verificare_il_titolo(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def verificare_correttezza(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def verificare_falso(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def verificare_uguale(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def verificare_non_uguale(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def aggiorna_la_pagina(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def ottenere_url_corrente(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def ottenere_la_pagina_html(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def indietro(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def avanti(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def è_testo_visto(self, *args, **kwargs):  # noqa
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def è_elemento_visto(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def è_elemento_presente(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def attendi_il_testo(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def attendere_un_elemento(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def attendere_un_elemento_presente(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def dormire(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def inviare(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def js_fare_clic(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def controlla_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def salva_screenshot(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def seleziona_file(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def esegui_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def bloccare_gli_annunci(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def saltare(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def verificare_i_collegamenti(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def controlla_errori_js(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def passa_al_frame(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def passa_al_contenuto_predefinito(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def apri_una_nuova_finestra(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def passa_alla_finestra(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def passa_alla_finestra_predefinita(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def illuminare(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def illuminare_clic(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def scorrere_fino_a(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def scorri_verso_alto(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def scorri_verso_il_basso(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def passa_il_mouse_sopra_e_fai_clic(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def è_selezionato(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def premere_la_freccia_su(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def premere_la_freccia_giù(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def premere_la_freccia_sinistra(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def premere_la_freccia_destra(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def fare_clic_sugli_elementi_visibili(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def selezionare_opzione_per_testo(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def selezionare_opzione_per_indice(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def selezionare_opzione_per_valore(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def creare_un_tour(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def creare_un_tour_shepherd(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def creare_un_tour_bootstrap(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def creare_un_tour_hopscotch(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def creare_un_tour_introjs(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def aggiungere_un_passo_al_tour(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def riprodurre_il_tour(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def esportare_il_tour(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def fallire(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def ottenere_url(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def visita_url(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def ottenere_elemento(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def trovare_elemento(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def ottenere_attributo(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def imposta_attributo(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def impostare_gli_attributi(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def digitare(self, *args, **kwargs):
        # input(selector, new_value)  # Same as update_text()
        return self.type(*args, **kwargs)

    def scrivere(self, *args, **kwargs):
        # write(selector, new_value)  # Same as update_text()
        return self.write(*args, **kwargs)

    def stampare(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)


class MasterQA_Italiano(MasterQA, CasoDiProva):

    def verificare(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Controllo manuale"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "La pagina ha un bell'aspetto?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
