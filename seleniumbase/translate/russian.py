# Russian / Русский - Translations
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class ТестНаСелен(BaseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._language = "Russian"

    def открыть(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def открыть_URL(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def нажмите(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def дважды_нажмите(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def нажмите_медленно(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def нажмите_если_виден(self, *args, **kwargs):
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def JS_нажмите_если_присутствует(self, *args, **kwargs):
        # js_click_if_present(selector, by=By.CSS_SELECTOR)
        return self.js_click_if_present(*args, **kwargs)

    def нажмите_ссылку(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def нажмите_на_местоположение(self, *args, **kwargs):
        # click_with_offset(selector, x, y, by=By.CSS_SELECTOR,
        #                   mark=None, timeout=None, center=None)
        return self.click_with_offset(*args, **kwargs)

    def обновить_текст(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def введите(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def добавить_текст(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def получить_текст(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def подтвердить_текст(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def подтвердить_текст_точно(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def подтвердить_ссылку(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def подтвердить_текст_не_виден(self, *args, **kwargs):
        # assert_text_not_visible(text, selector)
        return self.assert_text_not_visible(*args, **kwargs)

    def подтвердить_элемент(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def подтвердить_элемент_виден(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def подтвердить_элемент_не_виден(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def подтвердить_элемент_присутствует(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def подтвердить_элемент_отсутствует(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def подтвердить_атрибут(self, *args, **kwargs):
        # assert_attribute(selector, attribute, value)
        return self.assert_attribute(*args, **kwargs)

    def подтвердить_URL(self, *args, **kwargs):
        # assert_url(url)
        return self.assert_url(*args, **kwargs)

    def подтвердить_URL_содержит(self, *args, **kwargs):
        # assert_url_contains(substring)
        return self.assert_url_contains(*args, **kwargs)

    def подтвердить_название(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def подтвердить_название_содержит(self, *args, **kwargs):
        # assert_title_contains(substring)
        return self.assert_title_contains(*args, **kwargs)

    def получить_название(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def подтвердить_правду(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def подтвердить_ложные(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def подтвердить_одинаковый(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def подтвердить_не_одинаковый(self, *args, **kwargs):
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

    def точный_текст_виден(self, *args, **kwargs):
        # is_exact_text_visible(text, selector="html")
        return self.is_exact_text_visible(*args, **kwargs)

    def элемент_виден(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def элемент_включен(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def элемент_присутствует(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def ждать_текста(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def ждать_элемента(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def ждать_элемента_виден(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def ждать_элемента_не_виден(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def ждать_элемента_присутствует(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def ждать_элемента_отсутствует(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def ждать_атрибут(self, *args, **kwargs):
        # wait_for_attribute(selector, attribute, value)
        return self.wait_for_attribute(*args, **kwargs)

    def ждать_загрузки_страницы(self, *args, **kwargs):
        # wait_for_ready_state_complete()
        return self.wait_for_ready_state_complete(*args, **kwargs)

    def спать(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def ждать(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def отправить(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def очистить(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def сосредоточиться(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def JS_нажмите(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def JS_обновить_текст(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def JS_введите(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def проверить_HTML(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def сохранить_скриншот(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def сохранить_скриншот_в_логи(self, *args, **kwargs):
        # save_screenshot_to_logs(name)
        return self.save_screenshot_to_logs(*args, **kwargs)

    def выберите_файл(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def выполнение_скрипта(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def безопасное_выполнение_скрипта(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def активировать_JQUERY(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def активировать_RECORDER(self, *args, **kwargs):
        # activate_recorder()
        return self.activate_recorder(*args, **kwargs)

    def открыть_если_не_URL(self, *args, **kwargs):
        # open_if_not_url(url)
        return self.open_if_not_url(*args, **kwargs)

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

    def переключиться_на_родительский_кадр(self, *args, **kwargs):
        # switch_to_parent_frame()
        return self.switch_to_parent_frame(*args, **kwargs)

    def открыть_новое_окно(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def переключиться_на_окно(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def переключиться_на_окно_по_умолчанию(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def переключиться_на_последнее_окно(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def максимальное_окно(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

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

    def нажмите_видимые_элементы(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def выбрать_опцию_по_тексту(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def выбрать_опцию_по_индексу(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def выбрать_опцию_по_значению(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def создать_презентацию(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def добавить_слайд(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def сохранить_презентацию(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def начать_презентацию(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def создать_круговую_диаграмму(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def создать_бар_диаграмму(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def создать_столбчатую_диаграмму(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def создать_линейную_диаграмму(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def создать_диаграмму_области(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def добавить_серии_в_диаграмму(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def добавить_точку_данных(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def сохранить_диаграмму(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def отображать_диаграмму(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def извлекать_диаграмму(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def создать_тур(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def создать_SHEPHERD_тур(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def создать_BOOTSTRAP_тур(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def создать_DRIVERJS_тур(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def создать_HOPSCOTCH_тур(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def создать_INTROJS_тур(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def добавить_шаг_в_тур(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def играть_тур(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def экспортировать_тур(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def получить_текст_PDF(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def подтвердить_текст_PDF(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def скачать_файл(self, *args, **kwargs):
        # download_file(file)
        return self.download_file(*args, **kwargs)

    def загруженный_файл_присутствует(self, *args, **kwargs):
        # is_downloaded_file_present(file)
        return self.is_downloaded_file_present(*args, **kwargs)

    def получить_путь_к_загруженному_файлу(self, *args, **kwargs):
        # get_path_of_downloaded_file(file)
        return self.get_path_of_downloaded_file(*args, **kwargs)

    def подтвердить_загруженный_файл(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def удалить_загруженный_файл(self, *args, **kwargs):
        # delete_downloaded_file(file)
        return self.delete_downloaded_file(*args, **kwargs)

    def провалить(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def получить(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def посетить(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def посетить_URL(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def получить_элемент(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def найти_элемент(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def удалить_элемент(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def удалить_элементы(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def найти_текст(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def набор_текст(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def получить_атрибут(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def набор_атрибута(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def набор_атрибутов(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def написать(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def набор_тему_сообщения(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def показать_сообщение(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def печатать(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def отложенный_подтвердить_элемент(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def отложенный_подтвердить_текст(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def обработки_отложенных_подтверждений(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def принять_оповещение(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def увольнять_оповещение(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def переключиться_на_оповещение(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def перетащить_и_падение(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def набор_HTML(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def загрузить_HTML_файл(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def открыть_HTML_файл(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def удалить_все_куки(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def получить_агента_пользователя(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def получить_код_языка(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_Русский(MasterQA, ТестНаСелен):
    def подтвердить(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "Ручная проверка"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "Страница хорошо выглядит?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
