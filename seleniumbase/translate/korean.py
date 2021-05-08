# Korean / 한국어 - Translations - Python 3 Only!
from seleniumbase import BaseCase
from seleniumbase import MasterQA


class 셀레늄_테스트_케이스(BaseCase):  # noqa
    def __init__(self, *args, **kwargs):
        super(셀레늄_테스트_케이스, self).__init__(*args, **kwargs)
        self._language = "Korean"

    def 열기(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def URL_열기(self, *args, **kwargs):
        # open_url(url)
        return self.open_url(*args, **kwargs)

    def 클릭(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def 더블_클릭(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def 천천히_클릭(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def 보이는_경우_클릭(self, *args, **kwargs):
        # click_if_visible(selector, by=By.CSS_SELECTOR)
        return self.click_if_visible(*args, **kwargs)

    def 링크_텍스트를_클릭합니다(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def 텍스트를_업데이트(self, *args, **kwargs):
        # update_text(selector, text)
        return self.update_text(*args, **kwargs)

    def 입력(self, *args, **kwargs):
        # type(selector, text)  # Same as update_text()
        return self.type(*args, **kwargs)

    def 텍스트를_추가(self, *args, **kwargs):
        # add_text(selector, text)
        return self.add_text(*args, **kwargs)

    def 텍스트를_검색(self, *args, **kwargs):
        # get_text(selector, text)
        return self.get_text(*args, **kwargs)

    def 텍스트_확인(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def 정확한_텍스트를_확인하는(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def 링크_텍스트_확인(self, *args, **kwargs):
        # assert_link_text(link_text)
        return self.assert_link_text(*args, **kwargs)

    def 요소_확인(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def 요소가_보이는지_확인(self, *args, **kwargs):
        # assert_element_visible(selector)  # Same as self.assert_element()
        return self.assert_element_visible(*args, **kwargs)

    def 요소가_보이지_않는지_확인(self, *args, **kwargs):
        # assert_element_not_visible(selector)
        return self.assert_element_not_visible(*args, **kwargs)

    def 요소가_존재하는지_확인(self, *args, **kwargs):
        # assert_element_present(selector)
        return self.assert_element_present(*args, **kwargs)

    def 요소가_존재하지_않는지_확인(self, *args, **kwargs):
        # assert_element_absent(selector)
        return self.assert_element_absent(*args, **kwargs)

    def 특성_확인(self, *args, **kwargs):
        # assert_attribute(selector, attribute, value)
        return self.assert_attribute(*args, **kwargs)

    def 제목_확인(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def 제목_검색(self, *args, **kwargs):
        # get_title()
        return self.get_title(*args, **kwargs)

    def 올바른지_확인(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def 거짓인지_확인(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def 동일한지_확인(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def 동일하지_않다고_어설션(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def 페이지_새로_고침(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def 현재의_URL을_가져(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def 페이지의_소스_코드를_얻을(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def 뒤로(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def 앞으로(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def 텍스트가_표시됩니다(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def 요소가_표시됩니다(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def 요소가_활성화돼(self, *args, **kwargs):
        # is_element_enabled(selector)
        return self.is_element_enabled(*args, **kwargs)

    def 요소가_있습니다(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def 텍스트가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def 요소가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def 요소가_표시_될_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_element_visible(selector)  # Same as wait_for_element()
        return self.wait_for_element_visible(*args, **kwargs)

    def 요소가_사라질_때까지_기다리십시오(self, *args, **kwargs):
        # wait_for_element_not_visible(selector)
        return self.wait_for_element_not_visible(*args, **kwargs)

    def 요소가_존재할_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_element_present(selector)
        return self.wait_for_element_present(*args, **kwargs)

    def 요소가_나타날_때까지_기다리십시오(self, *args, **kwargs):
        # wait_for_element_absent(selector)
        return self.wait_for_element_absent(*args, **kwargs)

    def 특성_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_attribute(selector, attribute, value)
        return self.wait_for_attribute(*args, **kwargs)

    def 잠을(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def 기다림(self, *args, **kwargs):
        # wait(seconds)  # Same as sleep(seconds)
        return self.wait(*args, **kwargs)

    def 제출(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def 지우려면(self, *args, **kwargs):
        # clear(selector)
        return self.clear(*args, **kwargs)

    def 집중하다(self, *args, **kwargs):
        # focus(selector)
        return self.focus(*args, **kwargs)

    def JS_클릭(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def JS_텍스트를_업데이트(self, *args, **kwargs):
        # js_update_text(selector, text)
        return self.js_update_text(*args, **kwargs)

    def JS_입력(self, *args, **kwargs):
        # js_type(selector, text)
        return self.js_type(*args, **kwargs)

    def HTML_확인(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def 스크린_샷_저장(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def 로그에_스크린_샷_저장(self, *args, **kwargs):
        # save_screenshot_to_logs(name)
        return self.save_screenshot_to_logs(*args, **kwargs)

    def 파일을_선택(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def 스크립트를_실행하려면(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def 스크립트를_안전하게_실행(self, *args, **kwargs):
        # safe_execute_script(script)
        return self.safe_execute_script(*args, **kwargs)

    def JQUERY_로드(self, *args, **kwargs):
        # activate_jquery()
        return self.activate_jquery(*args, **kwargs)

    def 광고_차단(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def 건너뛸(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def 끊어진_링크_확인(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def JS_오류_확인(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def 프레임으로_전환(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def 기본_콘텐츠로_전환(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def 새_창_열기(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def 창으로_전환(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def 기본_창으로_전환(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def 최신_창으로_전환(self, *args, **kwargs):
        # switch_to_newest_window()
        return self.switch_to_newest_window(*args, **kwargs)

    def 창_최대화(self, *args, **kwargs):
        # maximize_window()
        return self.maximize_window(*args, **kwargs)

    def 강조(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def 강조_클릭(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def 요소로_스크롤(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def 맨_위로_스크롤(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def 하단으로_스크롤(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)

    def 위로_마우스를_이동하고_클릭(self, *args, **kwargs):
        # hover_and_click(hover_selector, click_selector)
        return self.hover_and_click(*args, **kwargs)

    def 선택되어_있는지(self, *args, **kwargs):
        # is_selected(selector)
        return self.is_selected(*args, **kwargs)

    def 위쪽_화살표를_누릅니다(self, *args, **kwargs):
        # press_up_arrow(selector="html", times=1)
        return self.press_up_arrow(*args, **kwargs)

    def 아래쪽_화살표를_누르십시오(self, *args, **kwargs):
        # press_down_arrow(selector="html", times=1)
        return self.press_down_arrow(*args, **kwargs)

    def 왼쪽_화살표를_누르십시오(self, *args, **kwargs):
        # press_left_arrow(selector="html", times=1)
        return self.press_left_arrow(*args, **kwargs)

    def 오른쪽_화살표를_누르십시오(self, *args, **kwargs):
        # press_right_arrow(selector="html", times=1)
        return self.press_right_arrow(*args, **kwargs)

    def 페이지_요소를_클릭_합니다(self, *args, **kwargs):
        # click_visible_elements(selector)
        return self.click_visible_elements(*args, **kwargs)

    def 텍스트로_옵션_선택(self, *args, **kwargs):
        # select_option_by_text(dropdown_selector, option)
        return self.select_option_by_text(*args, **kwargs)

    def 인덱스별로_옵션_선택(self, *args, **kwargs):
        # select_option_by_index(dropdown_selector, option)
        return self.select_option_by_index(*args, **kwargs)

    def 값별로_옵션_선택(self, *args, **kwargs):
        # select_option_by_value(dropdown_selector, option)
        return self.select_option_by_value(*args, **kwargs)

    def 프레젠테이션_만들기(self, *args, **kwargs):
        # create_presentation(name=None, theme="default", transition="default")
        return self.create_presentation(*args, **kwargs)

    def 슬라이드_추가(self, *args, **kwargs):
        # add_slide(content=None, image=None, code=None, iframe=None,
        #           content2=None, notes=None, transition=None, name=None)
        return self.add_slide(*args, **kwargs)

    def 프레젠테이션_저장(self, *args, **kwargs):
        # save_presentation(name=None, filename=None,
        #                   show_notes=False, interval=0)
        return self.save_presentation(*args, **kwargs)

    def 프레젠테이션_시작(self, *args, **kwargs):
        # begin_presentation(name=None, filename=None,
        #                    show_notes=False, interval=0)
        return self.begin_presentation(*args, **kwargs)

    def 원형_차트_만들기(self, *args, **kwargs):
        # create_pie_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_pie_chart(*args, **kwargs)

    def 막대_차트_만들기(self, *args, **kwargs):
        # create_bar_chart(chart_name=None, title=None, subtitle=None,
        #                  data_name=None, unit=None, libs=True)
        return self.create_bar_chart(*args, **kwargs)

    def 열_차트_만들기(self, *args, **kwargs):
        # create_column_chart(chart_name=None, title=None, subtitle=None,
        #                     data_name=None, unit=None, libs=True)
        return self.create_column_chart(*args, **kwargs)

    def 선_차트_만들기(self, *args, **kwargs):
        # create_line_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_line_chart(*args, **kwargs)

    def 영역_차트_만들기(self, *args, **kwargs):
        # create_area_chart(chart_name=None, title=None, subtitle=None,
        #                   data_name=None, unit=None, zero=False, libs=True)
        return self.create_area_chart(*args, **kwargs)

    def 차트에_시리즈_추가(self, *args, **kwargs):
        # add_series_to_chart(data_name=None, chart_name=None)
        return self.add_series_to_chart(*args, **kwargs)

    def 데이터_포인트_추가(self, *args, **kwargs):
        # add_data_point(label, value, color=None, chart_name=None)
        return self.add_data_point(*args, **kwargs)

    def 차트_저장(self, *args, **kwargs):
        # save_chart(chart_name=None, filename=None)
        return self.save_chart(*args, **kwargs)

    def 차트_표시(self, *args, **kwargs):
        # display_chart(chart_name=None, filename=None, interval=0)
        return self.display_chart(*args, **kwargs)

    def 차트_추출(self, *args, **kwargs):
        # extract_chart(chart_name=None)
        return self.extract_chart(*args, **kwargs)

    def 가이드_투어_만들기(self, *args, **kwargs):
        # create_tour(name=None, theme=None)
        return self.create_tour(*args, **kwargs)

    def 가이드_SHEPHERD_투어_만들기(self, *args, **kwargs):
        # create_shepherd_tour(name=None, theme=None)
        return self.create_shepherd_tour(*args, **kwargs)

    def 가이드_BOOTSTRAP_투어_만들기(self, *args, **kwargs):
        # create_bootstrap_tour(name=None, theme=None)
        return self.create_bootstrap_tour(*args, **kwargs)

    def 가이드_DRIVERJS_투어_만들기(self, *args, **kwargs):
        # create_driverjs_tour(name=None, theme=None)
        return self.create_driverjs_tour(*args, **kwargs)

    def 가이드_HOPSCOTCH_투어_만들기(self, *args, **kwargs):
        # create_hopscotch_tour(name=None, theme=None)
        return self.create_hopscotch_tour(*args, **kwargs)

    def 가이드_INTROJS_투어_만들기(self, *args, **kwargs):
        # create_introjs_tour(name=None, theme=None)
        return self.create_introjs_tour(*args, **kwargs)

    def 둘러보기_단계_추가(self, *args, **kwargs):
        # add_tour_step(message, selector=None, name=None,
        #               title=None, theme=None, alignment=None)
        return self.add_tour_step(*args, **kwargs)

    def 가이드_투어를하다(self, *args, **kwargs):
        # play_tour(name=None)
        return self.play_tour(*args, **kwargs)

    def 가이드_투어_내보내기(self, *args, **kwargs):
        # export_tour(name=None, filename="my_tour.js", url=None)
        return self.export_tour(*args, **kwargs)

    def PDF_텍스트를_검색(self, *args, **kwargs):
        # get_pdf_text(pdf, page=None, maxpages=None, password=None,
        #              codec='utf-8', wrap=False, nav=False, override=False)
        return self.get_pdf_text(*args, **kwargs)

    def PDF_텍스트_확인(self, *args, **kwargs):
        # assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
        #                 codec='utf-8', wrap=True, nav=False, override=False)
        return self.assert_pdf_text(*args, **kwargs)

    def 파일_다운로드(self, *args, **kwargs):
        # download_file(file)
        return self.download_file(*args, **kwargs)

    def 다운로드한_파일이_있습니다(self, *args, **kwargs):
        # is_downloaded_file_present(file)
        return self.is_downloaded_file_present(*args, **kwargs)

    def 다운로드한_파일_경로_가져_오기(self, *args, **kwargs):
        # get_path_of_downloaded_file(file)
        return self.get_path_of_downloaded_file(*args, **kwargs)

    def 다운로드한_파일_확인(self, *args, **kwargs):
        # assert_downloaded_file(file)
        return self.assert_downloaded_file(*args, **kwargs)

    def 다운로드한_파일_삭제(self, *args, **kwargs):
        # delete_downloaded_file(file)
        return self.delete_downloaded_file(*args, **kwargs)

    def 실패(self, *args, **kwargs):
        # fail(msg=None)  # Inherited from "unittest"
        return self.fail(*args, **kwargs)

    def 받기(self, *args, **kwargs):
        # get(url)  # Same as open(url)
        return self.get(*args, **kwargs)

    def 방문(self, *args, **kwargs):
        # visit(url)  # Same as open(url)
        return self.visit(*args, **kwargs)

    def 방문_URL(self, *args, **kwargs):
        # visit_url(url)  # Same as open(url)
        return self.visit_url(*args, **kwargs)

    def 요소_검색(self, *args, **kwargs):
        # get_element(selector)  # Element can be hidden
        return self.get_element(*args, **kwargs)

    def 요소를_찾을(self, *args, **kwargs):
        # find_element(selector)  # Element must be visible
        return self.find_element(*args, **kwargs)

    def 첫_번째_요소_제거(self, *args, **kwargs):
        # remove_element(selector)
        return self.remove_element(*args, **kwargs)

    def 모든_요소_제거(self, *args, **kwargs):
        # remove_elements(selector)
        return self.remove_elements(*args, **kwargs)

    def 텍스트_찾기(self, *args, **kwargs):
        # find_text(text, selector="html")  # Same as wait_for_text
        return self.find_text(*args, **kwargs)

    def 텍스트_설정(self, *args, **kwargs):
        # set_text(selector, text)
        return self.set_text(*args, **kwargs)

    def 특성_검색(self, *args, **kwargs):
        # get_attribute(selector, attribute)
        return self.get_attribute(*args, **kwargs)

    def 특성_설정(self, *args, **kwargs):
        # set_attribute(selector, attribute, value)
        return self.set_attribute(*args, **kwargs)

    def 모든_특성_설정(self, *args, **kwargs):
        # set_attributes(selector, attribute, value)
        return self.set_attributes(*args, **kwargs)

    def 쓰다(self, *args, **kwargs):
        # write(selector, text)  # Same as update_text()
        return self.write(*args, **kwargs)

    def 메시지_테마_설정(self, *args, **kwargs):
        # set_messenger_theme(theme="default", location="default")
        return self.set_messenger_theme(*args, **kwargs)

    def 메시지를_표시(self, *args, **kwargs):
        # post_message(message, duration=None, pause=True, style="info")
        return self.post_message(*args, **kwargs)

    def 인쇄(self, *args, **kwargs):
        # _print(msg)  # Same as Python print()
        return self._print(*args, **kwargs)

    def 연기된_요소_확인(self, *args, **kwargs):
        # deferred_assert_element(selector)
        return self.deferred_assert_element(*args, **kwargs)

    def 연기된_텍스트_확인(self, *args, **kwargs):
        # deferred_assert_text(text, selector="html")
        return self.deferred_assert_text(*args, **kwargs)

    def 연기된_검증_처리(self, *args, **kwargs):
        # process_deferred_asserts(print_only=False)
        return self.process_deferred_asserts(*args, **kwargs)

    def 경고를_수락(self, *args, **kwargs):
        # accept_alert(timeout=None)
        return self.accept_alert(*args, **kwargs)

    def 경고를_거부(self, *args, **kwargs):
        # dismiss_alert(timeout=None)
        return self.dismiss_alert(*args, **kwargs)

    def 경고로_전환(self, *args, **kwargs):
        # switch_to_alert(timeout=None)
        return self.switch_to_alert(*args, **kwargs)

    def 드래그_앤_드롭(self, *args, **kwargs):
        # drag_and_drop(drag_selector, drop_selector)
        return self.drag_and_drop(*args, **kwargs)

    def HTML_설정(self, *args, **kwargs):
        # set_content(html_string, new_page=False)
        return self.set_content(*args, **kwargs)

    def HTML_파일_로드(self, *args, **kwargs):
        # load_html_file(html_file, new_page=True)
        return self.load_html_file(*args, **kwargs)

    def HTML_파일_열기(self, *args, **kwargs):
        # open_html_file(html_file)
        return self.open_html_file(*args, **kwargs)

    def 모든_쿠키_삭제(self, *args, **kwargs):
        # delete_all_cookies()
        return self.delete_all_cookies(*args, **kwargs)

    def 사용자_에이전트_가져_오기(self, *args, **kwargs):
        # get_user_agent()
        return self.get_user_agent(*args, **kwargs)

    def 언어_코드를_얻을(self, *args, **kwargs):
        # get_locale_code()
        return self.get_locale_code(*args, **kwargs)


class MasterQA_한국어(MasterQA, 셀레늄_테스트_케이스):
    def 확인(self, *args, **kwargs):
        # "Manual Check"
        self.DEFAULT_VALIDATION_TITLE = "수동 검사"
        # "Does the page look good?"
        self.DEFAULT_VALIDATION_MESSAGE = "페이지가 잘 보이나요?"
        # verify(QUESTION)
        return self.verify(*args, **kwargs)
