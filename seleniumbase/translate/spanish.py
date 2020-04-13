# Spanish / español - Translations - Python 3 Only!
from seleniumbase import BaseCase


class CasoDePrueba(BaseCase):

    def abrir_url(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def haga_clic(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def doble_clic(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def haga_clic_lentamente(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def haga_clic_en_el_texto_del_enlace(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def actualizar_texto(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def agregar_texto(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def obtener_texto(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def verificar_texto(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def verificar_texto_exacto(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def verificar_elemento(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def verificar_título(self, *args, **kwargs):  # noqa
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

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

    def está_presente_el_elemento(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def espere_el_texto(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def espere_el_elemento(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def dormir(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def enviar(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def js_haga_clic(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

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

    def bloquear_anuncios(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def omitir(self, *args, **kwargs):
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

    def cambiar_a_la_ventana(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def cambiar_a_la_ventana_predeterminada(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def resaltar(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def resalte_y_haga_clic(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def desplazarse_a(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def desplazarse_a_la_parte_superior(self, *args, **kwargs):
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
        return self.is_selected(*args, **kwargs)

    def presione_la_flecha_hacia_abajo(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)

    def presione_la_flecha_izquierda(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)

    def presione_la_flecha_derecha(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)
