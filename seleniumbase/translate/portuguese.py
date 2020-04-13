# Portuguese / Português - Translations - Python 3 Only!
from seleniumbase import BaseCase


class CasoDeTeste(BaseCase):

    def abrir_url(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def clique(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def clique_duas_vezes(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def clique_devagar(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def clique_no_texto_do_link(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def atualizar_texto(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def adicionar_texto(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def obter_texto(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def verificar_texto(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def verifique_texto_exato(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def verificar_elemento(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def verificar_título(self, *args, **kwargs):  # noqa
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def verificar_verdade(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def verificar_falso(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def verificar_igual(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def verificar_não_é_igual(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def atualizar_a_página(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def obter_url_atual(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def obter_a_página_html(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def voltar(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def avançar(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def o_texto_está_visível(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def o_elemento_está_visível(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def o_elemento_está_presente(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def aguarde_o_texto(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def aguardar_o_elemento(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def dormir(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def enviar(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def js_clique(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def verificar_html(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def salvar_captura_de_tela(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def selecionar_arquivo(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def executar_o_script(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def bloquear_anúncios(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def omitir(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def verifique_se_há_links_quebrados(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def verifique_se_há_erros_de_js(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def mudar_para_o_quadro(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def volte_para_o_conteúdo_padrão(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def abrir_nova_janela(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def mudar_para_janela(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def volte_para_a_janela_padrão(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def destaque(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def destaque_e_clique(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def rolar_para(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def rolar_para_o_topo(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def rolar_para_o_fundo(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def passe_o_mouse_e_clique(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def é_selecionado(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def pressione_a_seta_para_cima(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)

    def pressione_a_seta_para_baixo(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)

    def pressione_a_seta_esquerda(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)

    def pressione_a_seta_direita(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.is_selected(*args, **kwargs)
