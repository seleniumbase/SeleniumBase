# Dutch / Nederlands - Translations
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class Testgeval(BaseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._language = "Dutch"

    def openen(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def url_openen(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def klik(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def dubbelklik(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def contextklik(self, *args, **kwargs):
        # context_click(selector)
        return self.context_click(*args, **kwargs)

    def klik_langzaam(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def klik_indien_zichtbaar(self, *args, **kwargs):
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def js_klik_indien_aanwezig(self, *args, **kwargs):
        # js_click_if_present(selector, by=By.CSS_SELECTOR)
        return self.js_click_if_present(*args, **kwargs)

    def klik_linktekst(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def klik_op_locatie(self, *args, **kwargs):
        # click_with_offset(selector, x, y, by=By.CSS_SELECTOR,
        #                   mark=None, timeout=None, center=None)
        return self.click_with_offset(*args, **kwargs)

    def tekst_bijwerken(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def typ(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def tekst_toevoegen(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def tekst_ophalen(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def controleren_tekst(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def controleren_exacte_tekst(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def controleren_linktekst(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def controleren_niet_lege_tekst(self, *args, **kwargs):
        # assert_non_empty_text(selector)
        return self.assert_non_empty_text(*args, **kwargs)

    def controleren_tekst_niet_zichtbaar(self, *args, **kwargs):
        # assert_text_not_visible(text, selector)
        return self.assert_text_not_visible(*args, **kwargs)

    def controleren_element(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def controleren_element_zichtbaar(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def controleren_element_niet_zichtbaar(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def controleren_element_aanwezig(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def controleren_element_afwezig(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def controleren_attribuut(self, *args, **kwargs):
        # assert_attribute(selector, attribute, value)
        return self.assert_attribute(*args, **kwargs)

    def controleren_url(self, *args, **kwargs):
        # assert_url(url)
        return self.assert_url(*args, **kwargs)

    def controleren_url_bevat(self, *args, **kwargs):
        # assert_url_contains(substring)
        return self.assert_url_contains(*args, **kwargs)

    def controleren_titel(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def controleren_titel_bevat(self, *args, **kwargs):
        # assert_title_contains(substring)
        return self.assert_title_contains(*args, **kwargs)

    def titel_ophalen(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def controleren_ware(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def controleren_valse(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def controleren_gelijk(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def controleren_niet_gelijk(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def ververs_pagina(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def huidige_url_ophalen(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def broncode_ophalen(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def terug(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def vooruit(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def tekst_zichtbaar(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def exacte_tekst_zichtbaar(self, *args, **kwargs):
        # is_exact_text_visible(text, selector="html")
        return self.is_exact_text_visible(*args, **kwargs)

    def element_zichtbaar(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def element_ingeschakeld(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def element_aanwezig(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def wachten_op_tekst(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def wachten_op_element(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def wachten_op_element_zichtbaar(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def wachten_op_element_niet_zichtbaar(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def wachten_op_element_aanwezig(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def wachten_op_element_afwezig(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def wachten_op_attribuut(self, *args, **kwargs):
        # wait_for_attribute(selector, attribute, value)
        return self.wait_for_attribute(*args, **kwargs)

    def wacht_tot_de_pagina_is_geladen(self, *args, **kwargs):
        # wait_for_ready_state_complete()
        return self.wait_for_ready_state_complete(*args, **kwargs)

    def slapen(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def wachten(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def verzenden(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def wissen(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def focussen(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def js_klik(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def js_tekst_bijwerken(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def js_typ(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def jquery_klik(self, *args, **kwargs):
        # jquery_click(selector)
        return self.jquery_click(*args, **kwargs)

    def jquery_tekst_bijwerken(self, *args, **kwargs):
        # jquery_update_text(selector, text)
        return self.jquery_update_text(*args, **kwargs)

    def jquery_typ(self, *args, **kwargs):
        # jquery_type(selector, text)
        return self.jquery_type(*args, **kwargs)

    def html_inspecteren(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def bewaar_screenshot(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def bewaar_screenshot_om_te_loggen(self, *args, **kwargs):
        # save_screenshot_to_logs(name)
        return self.save_screenshot_to_logs(*args, **kwargs)

    def selecteer_bestand(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def script_uitvoeren(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def script_veilig_uitvoeren(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def activeer_jquery(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def activeer_recorder(self, *args, **kwargs):
        # activate_recorder()
        return self.activate_recorder(*args, **kwargs)

    def openen_zo_niet_url(self, *args, **kwargs):
        # open_if_not_url(url)
        return self.open_if_not_url(*args, **kwargs)

    def blokkeer_advertenties(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def overslaan(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def controleren_op_gebroken_links(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def controleren_op_js_fouten(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def overschakelen_naar_frame(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def overschakelen_naar_standaardcontent(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def overschakelen_naar_bovenliggend_frame(self, *args, **kwargs):
        # switch_to_parent_frame()
        return self.switch_to_parent_frame(*args, **kwargs)

    def nieuw_venster_openen(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def overschakelen_naar_venster(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def overschakelen_naar_standaardvenster(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def overschakelen_naar_nieuwste_venster(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def venster_maximaliseren(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

    def markeren(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def markeren_klik(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def scrollen_naar(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def naar_boven_scrollen(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def naar_beneden_scrollen(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def zweven_en_klik(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def zweven(self, *args, **kwargs):
        # hover(selector)
        return self.hover(*args, **kwargs)

    def is_het_geselecteerd(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def druk_op_pijl_omhoog(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def druk_op_pijl_omlaag(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def druk_op_pijl_links(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def druk_op_pijl_rechts(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def klik_zichtbare_elementen(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def optie_selecteren_op_tekst(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def optie_selecteren_op_index(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def optie_selecteren_op_waarde(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def maak_een_presentatie(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def een_dia_toevoegen(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def de_presentatie_opslaan(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def de_presentatie_starten(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def maak_een_cirkeldiagram(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def maak_een_staafdiagram(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def maak_een_kolomdiagram(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def maak_een_lijndiagram(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def maak_een_vlakdiagram(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def reeksen_toevoegen_aan_grafiek(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def gegevenspunt_toevoegen(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def grafiek_opslaan(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def grafiek_weergeven(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def grafiek_uitpakken(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def maak_een_tour(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def maak_een_shepherd_tour(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def maak_een_bootstrap_tour(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def maak_een_driverjs_tour(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def maak_een_hopscotch_tour(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def maak_een_introjs_tour(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def toevoegen_tour_stap(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def speel_de_tour(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def de_tour_exporteren(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def pdf_tekst_ophalen(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def controleren_pdf_tekst(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def bestand_downloaden(self, *args, **kwargs):
        # download_file(file)
        return self.download_file(*args, **kwargs)

    def gedownloade_bestand_aanwezig(self, *args, **kwargs):
        # is_downloaded_file_present(file)
        return self.is_downloaded_file_present(*args, **kwargs)

    def pad_gedownloade_bestand_ophalen(self, *args, **kwargs):
        # get_path_of_downloaded_file(file)
        return self.get_path_of_downloaded_file(*args, **kwargs)

    def controleren_gedownloade_bestand(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def verwijder_gedownloade_bestand(self, *args, **kwargs):
        # delete_downloaded_file(file)
        return self.delete_downloaded_file(*args, **kwargs)

    def mislukken(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def ophalen(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def bezoek(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def bezoek_url(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def element_ophalen(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def vind_element(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def verwijder_element(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def verwijder_elementen(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def vind_tekst(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def tekst_instellen(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def attribuut_ophalen(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def attribuut_instellen(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def attributen_instellen(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def schrijven(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def thema_van_bericht_instellen(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def bericht_weergeven(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def afdrukken(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def uitgestelde_controleren_element(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def uitgestelde_controleren_tekst(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def verwerken_uitgestelde_controleren(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def waarschuwing_accepteren(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def waarschuwing_wegsturen(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def overschakelen_naar_waarschuwing(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def slepen_en_neerzetten(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def html_instellen(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def html_bestand_laden(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def html_bestand_openen(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def alle_cookies_verwijderen(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def gebruikersagent_ophalen(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def taalcode_ophalen(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_Nederlands(MasterQA, Testgeval):
    def controleren(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Handmatige controle"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "Ziet de pagina er goed uit?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
