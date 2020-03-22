# Japanese Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class セレニウムテストケース(BaseCase):  # noqa

    def URLを開く(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def クリックして(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def ダブルクリックして(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def ゆっくりクリックして(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def リンクテキストをクリックします(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def テキストを更新(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def テキストを追加(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def テキストを取得(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def テキストを確認する(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def 正確なテキストを確認する(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def 要素を確認する(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def タイトルを確認(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def 検証が正しい(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def 検証は偽です(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def 検証が等しい(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def 検証が等しくない(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def ページを更新する(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def 現在のURLを取得(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def ページのソースコードを取得する(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def 戻る(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def 進む(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def テキストが表示されています(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def 要素は表示されますか(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def 要素が存在するかどうか(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def テキストを待つ(self, *args, **kwargs):
        # wait_for_text(text, selector)
        return self.wait_for_text(*args, **kwargs)

    def 要素を待つ(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def 眠る(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def を提出す(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def JSクリックして(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def htmlをチェック(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def スクリーンショットを保存(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def ファイルを選択(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def スクリプトを実行する(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def 広告ブロック(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def スキップする(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def リンク切れを確認する(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def JSエラーを確認する(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def フレームに切り替え(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def デフォルトのコンテンツに切り替える(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def 新しいウィンドウを開く(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def ウィンドウに切り替え(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def デフォルトのウィンドウに切り替える(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def ハイライト(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def ハイライトしてクリックして(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def スクロールして(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def 一番上までスクロール(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def 一番下までスクロール(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)
