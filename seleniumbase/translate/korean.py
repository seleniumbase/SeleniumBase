# Korean Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class 셀레늄_테스트_케이스(BaseCase):  # noqa

    def URL_열기(self, *args, **kwargs):
        # open(url)
        self.open(*args, **kwargs)

    def 클릭(self, *args, **kwargs):
        # click(selector)
        self.click(*args, **kwargs)

    def 더블_클릭(self, *args, **kwargs):
        # double_click(selector)
        self.double_click(*args, **kwargs)

    def 천천히_클릭(self, *args, **kwargs):
        # slow_click(selector)
        self.slow_click(*args, **kwargs)

    def 링크_텍스트를_클릭합니다(self, *args, **kwargs):
        # click_link_text(link_text)
        self.click_link_text(*args, **kwargs)

    def 텍스트를_업데이트(self, *args, **kwargs):
        # update_text(selector, new_value)
        self.update_text(*args, **kwargs)

    def 텍스트를_추가(self, *args, **kwargs):
        # add_text(selector, new_value)
        self.add_text(*args, **kwargs)

    def 텍스트를_검색(self, *args, **kwargs):
        # get_text(selector, new_value)
        self.get_text(*args, **kwargs)

    def 텍스트_확인(self, *args, **kwargs):
        # assert_text(text, selector)
        self.assert_text(*args, **kwargs)

    def 정확한_텍스트를_확인하는(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        self.assert_exact_text(*args, **kwargs)

    def 요소_확인(self, *args, **kwargs):
        # assert_element(selector)
        self.assert_element(*args, **kwargs)

    def 제목_확인(self, *args, **kwargs):
        # assert_title(title)
        self.assert_title(*args, **kwargs)

    def 올바른지_확인(self, *args, **kwargs):
        # assert_true(expr)
        self.assert_true(*args, **kwargs)

    def 거짓인지_확인(self, *args, **kwargs):
        # assert_false(expr)
        self.assert_false(*args, **kwargs)

    def 동일한지_확인(self, *args, **kwargs):
        # assert_equal(first, second)
        self.assert_equal(*args, **kwargs)

    def 동일하지_않다고_어설션(self, *args, **kwargs):
        # assert_not_equal(first, second)
        self.assert_not_equal(*args, **kwargs)

    def 페이지_새로_고침(self, *args, **kwargs):
        # refresh_page()
        self.refresh_page(*args, **kwargs)

    def 현재의_URL을_가져(self, *args, **kwargs):
        # get_current_url()
        self.get_current_url(*args, **kwargs)

    def 페이지의_소스_코드를_얻을(self, *args, **kwargs):
        # get_page_source()
        self.get_page_source(*args, **kwargs)

    def 뒤로(self, *args, **kwargs):
        # go_back()
        self.go_back(*args, **kwargs)

    def 앞으로(self, *args, **kwargs):
        # go_forward()
        self.go_forward(*args, **kwargs)

    def 텍스트가_표시됩니다(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        self.is_text_visible(*args, **kwargs)

    def 요소가_표시됩니다(self, *args, **kwargs):
        # is_element_visible(selector)
        self.is_element_visible(*args, **kwargs)

    def 요소가_있습니다(self, *args, **kwargs):
        # is_element_present(selector)
        self.is_element_present(*args, **kwargs)

    def 텍스트가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_text(text, selector)
        self.wait_for_text(*args, **kwargs)

    def 요소가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_element(selector)
        self.wait_for_element(*args, **kwargs)

    def 잠을(self, *args, **kwargs):
        # sleep(seconds)
        self.sleep(*args, **kwargs)

    def 제출(self, *args, **kwargs):
        # submit(selector)
        self.submit(*args, **kwargs)

    def JS_클릭(self, *args, **kwargs):
        # js_click(selector)
        self.js_click(*args, **kwargs)

    def HTML_확인(self, *args, **kwargs):
        # inspect_html()
        self.inspect_html(*args, **kwargs)

    def 스크린_샷_저장(self, *args, **kwargs):
        # save_screenshot(name)
        self.save_screenshot(*args, **kwargs)

    def 파일을_선택(self, *args, **kwargs):
        # choose_file(selector, file_path)
        self.choose_file(*args, **kwargs)

    def 스크립트를_실행하려면(self, *args, **kwargs):
        # execute_script(script)
        self.execute_script(*args, **kwargs)

    def 광고_차단(self, *args, **kwargs):
        # ad_block()
        self.ad_block(*args, **kwargs)

    def 건너_뛰기(self, *args, **kwargs):
        # skip(reason="")
        self.skip(*args, **kwargs)

    def 끊어진_링크_확인(self, *args, **kwargs):
        # assert_no_404_errors()
        self.assert_no_404_errors(*args, **kwargs)

    def JS_오류_확인(self, *args, **kwargs):
        # assert_no_js_errors()
        self.assert_no_js_errors(*args, **kwargs)

    def 프레임으로_전환(self, *args, **kwargs):
        # switch_to_frame(frame)
        self.switch_to_frame(*args, **kwargs)

    def 기본_콘텐츠로_전환(self, *args, **kwargs):
        # switch_to_default_content()
        self.switch_to_default_content(*args, **kwargs)

    def 새_창_열기(self, *args, **kwargs):
        # open_new_window()
        self.open_new_window(*args, **kwargs)

    def 창으로_전환(self, *args, **kwargs):
        # switch_to_window(window)
        self.switch_to_window(*args, **kwargs)

    def 기본_창으로_전환(self, *args, **kwargs):
        # switch_to_default_window()
        self.switch_to_default_window(*args, **kwargs)

    def 강조(self, *args, **kwargs):
        # highlight(selector)
        self.highlight(*args, **kwargs)

    def 강조_클릭(self, *args, **kwargs):
        # highlight_click(selector)
        self.highlight_click(*args, **kwargs)

    def 요소로_스크롤(self, *args, **kwargs):
        # scroll_to(selector)
        self.scroll_to(*args, **kwargs)

    def 맨_위로_스크롤(self, *args, **kwargs):
        # scroll_to_top()
        self.scroll_to_top(*args, **kwargs)

    def 하단으로_스크롤(self, *args, **kwargs):
        # scroll_to_bottom()
        self.scroll_to_bottom(*args, **kwargs)
