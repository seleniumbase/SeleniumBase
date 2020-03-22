# Korean Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class 셀레늄_테스트_케이스(BaseCase):  # noqa

    def URL_열기(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def 클릭(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def 더블_클릭(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def 천천히_클릭(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def 링크_텍스트를_클릭합니다(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def 텍스트를_업데이트(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def 텍스트를_추가(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def 텍스트를_검색(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def 텍스트_확인(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def 정확한_텍스트를_확인하는(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def 요소_확인(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def 제목_확인(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

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

    def 요소가_있습니다(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def 텍스트가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def 요소가_나타날_때까지_기다립니다(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def 잠을(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def 제출(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def JS_클릭(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def HTML_확인(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def 스크린_샷_저장(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def 파일을_선택(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def 스크립트를_실행하려면(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def 광고_차단(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def 건너_뛰기(self, *args, **kwargs):
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
