# Spanish / Español - Translations - Python 3 Only!
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class CasoDePrueba(BaseCase):

    def __init__(self, *args, **kwargs):
        super(CasoDePrueba, self).__init__(*args, **kwargs)
        self._language = "Spanish"

    def abrir(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def abrir_url(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def haga_clic(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def doble_clic(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def clic_lentamente(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def clic_si_está_muestra(self, *args, **kwargs):  # noqa
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def clic_texto_del_enlace(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def actualizar_texto(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def escriba(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def agregar_texto(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def obtener_texto(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def verificar_texto(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def verificar_texto_exacto(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def verificar_texto_del_enlace(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def verificar_elemento(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def verificar_elemento_se_muestra(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def verificar_elemento_no_se_muestra(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def verificar_elemento_presente(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def verificar_elemento_ausente(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def verificar_título(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def obtener_título(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def verificar_verdad(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def verificar_falso(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def verificar_igual(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def verificar_diferente(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def actualizar_la_página(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def obtener_url_actual(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def obtener_html_de_la_página(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def volver(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def adelante(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def se_muestra_el_texto(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def se_muestra_el_elemento(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def está_habilitado_el_elemento(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def está_presente_el_elemento(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def espera_el_texto(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def espera_el_elemento(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def espera_el_elemento_se_muestra(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def espera_el_elemento_no_se_muestra(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def espera_el_elemento_presente(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def espera_el_elemento_ausente(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def dormir(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def espera(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def enviar(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def despejar(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def centrarse(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def js_haga_clic(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def js_actualizar_texto(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def js_escriba(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def comprobar_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def guardar_captura_de_pantalla(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def seleccionar_archivo(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def ejecutar_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def ejecutar_script_de_forma_segura(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def activar_jquery(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def bloquear_anuncios(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def saltar(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def verificar_si_hay_enlaces_rotos(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def verificar_si_hay_errores_js(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def cambiar_al_marco(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def cambiar_al_contenido_predeterminado(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def abrir_una_nueva_ventana(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def cambiar_a_ventana(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def cambiar_a_ventana_predeterminada(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def cambiar_a_ventana_última(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def maximizar_ventana(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

    def resalte(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def resalte_clic(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def desplazarse_a(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def desplazarse_hasta_la_parte_superior(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def desplazarse_hasta_la_parte_inferior(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def pasar_el_ratón_y_hacer_clic(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def está_seleccionado(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def presione_la_flecha_hacia_arriba(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def presione_la_flecha_hacia_abajo(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def presione_la_flecha_izquierda(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def presione_la_flecha_derecha(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def clic_en_elementos_visibles(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def seleccionar_opción_por_texto(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def seleccionar_opción_por_índice(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def seleccionar_opción_por_valor(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def crear_una_presentación(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def agregar_una_diapositiva(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def guardar_presentación(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def iniciar_presentación(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def crear_un_gráfico_circular(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def crear_un_gráfico_de_barras(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def crear_un_gráfico_de_columnas(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def crear_un_gráfico_de_líneas(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def crear_un_gráfico_de_área(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def agregar_series_al_gráfico(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def agregar_punto_de_datos(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def guardar_gráfico(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def muestra_gráfico(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def extracto_gráfico(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def crear_una_gira(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def crear_una_gira_shepherd(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def crear_una_gira_bootstrap(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def crear_una_gira_driverjs(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def crear_una_gira_hopscotch(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def crear_una_gira_introjs(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def agregar_paso_a_la_gira(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def reproducir_la_gira(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def exportar_la_gira(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def obtener_texto_pdf(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def verificar_texto_pdf(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def verificar_archivo_descargado(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def fallar(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def obtener(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def visita(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def visita_url(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def obtener_elemento(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def encontrar_elemento(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def eliminar_elemento(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def eliminar_elementos(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def encontrar_texto(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def establecer_texto(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def obtener_atributo(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def establecer_atributo(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def establecer_atributos(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def escribir(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def establecer_tema_del_mensaje(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def mostrar_mensaje(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def imprimir(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def diferido_verificar_elemento(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def diferido_verificar_texto(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def procesar_verificaciones_diferidas(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def aceptar_alerta(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def descartar_alerta(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def cambiar_a_alerta(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def arrastrar_y_soltar(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def establecer_html(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def cargar_archivo_html(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def abrir_archivo_html(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def eliminar_todas_las_cookies(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def obtener_agente_de_usuario(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def obtener_código_de_idioma(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_Español(MasterQA, CasoDePrueba):

    def verificar(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Comprobación manual"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "¿Se ve bien la página?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
