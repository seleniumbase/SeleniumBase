# Russian / Русский - Translations - Python 3 Only!
from seleniumbase import BaseCase


class ТестНаСелен(BaseCase):  # noqa

    def открытый(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def нажмите(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def дважды_нажмите(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def нажмите_медленно(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def нажмите_на_ссылку(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def обновить_текст(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def добавить_текст(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def получить_текст(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def проверить_текст(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def проверить_текст_точно(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def проверить_элемент(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def проверить_название(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def проверить_правду(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def проверить_ложные(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def проверить_одинаковый(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def проверить_не_одинаковый(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def обновить_страницу(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def получить_текущий_URL(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def получить_источник_страницы(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def назад(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def вперед(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def текст_виден(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def элемент_виден(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def элемент_присутствует(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def ждать_текста(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def ждать_элемента(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def спать(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def представить(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def JS_нажмите(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def проверять_HTML(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def сохранить_скриншот(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def выберите_файл(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def выполнить_скрипт(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def блокировать_рекламу(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def пропускать(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def проверить_ошибки_404(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def проверить_ошибки_JS(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def переключиться_на_кадр(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def переключиться_на_содержимое_по_умолчанию(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def открыть_новое_окно(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def переключиться_на_окно(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def переключиться_в_окно_по_умолчанию(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def осветить(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def осветить_нажмите(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def прокрутить_к(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def пролистать_наверх(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def прокрутить_вниз(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def наведите_и_нажмите(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def выбран(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def нажмите_стрелку_вверх(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def нажмите_стрелку_вниз(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def нажмите_стрелку_влево(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def нажмите_стрелку_вправо(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def выбрать_опцию_по_тексту(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def выбрать_опцию_по_индексу(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def выбрать_опцию_по_значению(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)
