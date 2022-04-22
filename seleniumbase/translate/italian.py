# Italian / Italiano - Translations - Python 3 Only!
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class CasoDiProva(BaseCase):
    def __init__(self, *args, **kwargs):
        super(CasoDiProva, self).__init__(*args, **kwargs)
        self._language = "Italian"

    def apri(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def apri_url(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def fare_clic(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def doppio_clic(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def clic_lentamente(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def clic_se_visto(self, *args, **kwargs):
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def clic_testo_del_collegamento(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def aggiornare_testo(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def digitare(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def aggiungi_testo(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def ottenere_testo(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def verificare_testo(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def verificare_testo_esatto(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def verificare_testo_del_collegamento(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def verificare_elemento(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def verificare_elemento_visto(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def verificare_elemento_non_visto(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def verificare_elemento_presente(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def verificare_elemento_assente(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def verificare_attributo(self, *args, **kwargs):
        # assert_attribute(selector, attribute, value)
        return self.assert_attribute(*args, **kwargs)

    def verificare_titolo(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def ottenere_titolo(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def verificare_vero(self, *args, **kwargs):
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

    def è_elemento_abilitato(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def è_elemento_presente(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def attendere_il_testo(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def attendere_un_elemento(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def attendere_un_elemento_visto(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def attendere_un_elemento_non_visto(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def attendere_un_elemento_presente(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def attendere_un_elemento_assente(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def attendere_un_attributo(self, *args, **kwargs):
        # wait_for_attribute(selector, attribute, value)
        return self.wait_for_attribute(*args, **kwargs)

    def dormire(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def attendere(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def inviare(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def cancellare(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def focalizzare(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def js_fare_clic(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def js_aggiornare_testo(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def js_digitare(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def controlla_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def salva_screenshot(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def salva_screenshot_nei_logs(self, *args, **kwargs):
        # save_screenshot_to_logs(name)
        return self.save_screenshot_to_logs(*args, **kwargs)

    def seleziona_file(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def eseguire_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def eseguire_script_sicuro(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def attiva_jquery(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def attiva_recorder(self, *args, **kwargs):
        # activate_recorder()
        return self.activate_recorder(*args, **kwargs)

    def apri_se_non_url(self, *args, **kwargs):
        # open_if_not_url(url)
        return self.open_if_not_url(*args, **kwargs)

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

    def passa_alla_cornice(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def passa_al_contenuto_predefinito(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def passa_alla_cornice_principale(self, *args, **kwargs):
        # switch_to_parent_frame()
        return self.switch_to_parent_frame(*args, **kwargs)

    def apri_una_nuova_finestra(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def passa_alla_finestra(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def passa_alla_finestra_predefinita(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def passa_alla_finestra_ultimo(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def ingrandisci_finestra(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

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

    def clic_sugli_elementi_visibili(self, *args, **kwargs):
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

    def creare_una_presentazione(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def aggiungere_una_diapositiva(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def salva_la_presentazione(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def avviare_la_presentazione(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def creare_un_grafico_a_torta(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def creare_un_grafico_a_barre(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def creare_un_grafico_a_colonne(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def creare_un_grafico_a_linee(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def creare_un_grafico_ad_area(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def aggiungere_serie_al_grafico(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def aggiungi_punto_dati(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def salva_il_grafico(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def mostra_il_grafico(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def estrarre_il_grafico(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def creare_un_tour(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def creare_un_tour_shepherd(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def creare_un_tour_bootstrap(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def creare_un_tour_driverjs(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def creare_un_tour_hopscotch(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def creare_un_tour_introjs(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def aggiungere_passo_al_tour(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def riprodurre_il_tour(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def esportare_il_tour(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def ottenere_testo_pdf(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def verificare_testo_pdf(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def scaricare_file(self, *args, **kwargs):
        # download_file(file)
        return self.download_file(*args, **kwargs)

    def è_file_scaricato_presente(self, *args, **kwargs):
        # is_downloaded_file_present(file)
        return self.is_downloaded_file_present(*args, **kwargs)

    def ottenere_percorso_del_file_scaricato(self, *args, **kwargs):
        # get_path_of_downloaded_file(file)
        return self.get_path_of_downloaded_file(*args, **kwargs)

    def verificare_file_scaricato(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def eliminare_file_scaricato(self, *args, **kwargs):
        # delete_downloaded_file(file)
        return self.delete_downloaded_file(*args, **kwargs)

    def fallire(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def ottenere(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def visita(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def visita_url(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def ottenere_elemento(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def trovare_elemento(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def rimuovere_elemento(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def rimuovere_elementi(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def trovare_testo(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def impostare_testo(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def ottenere_attributo(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def imposta_attributo(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def impostare_gli_attributi(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def scrivere(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def impostare_tema_del_messaggio(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def visualizza_messaggio(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def stampare(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def differita_verificare_elemento(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def differita_verificare_testo(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def elaborare_differita_verificari(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def accetta_avviso(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def elimina_avviso(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def passa_al_avviso(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def trascinare_e_rilasciare(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def impostare_html(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def caricare_html_file(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def apri_html_file(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def elimina_tutti_i_cookie(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def ottenere_agente_utente(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def ottenere_codice_lingua(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_Italiano(MasterQA, CasoDiProva):
    def verificare(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Controllo manuale"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "La pagina ha un bell'aspetto?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
