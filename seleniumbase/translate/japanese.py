# Japanese Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class セレニウムテストケース(BaseCase):  # noqa

    def URLを開く(self, *args, **kwargs):
        # open(url)
        self.open(*args, **kwargs)

    def クリックして(self, *args, **kwargs):
        # click(selector)
        self.click(*args, **kwargs)

    def ダブルクリックして(self, *args, **kwargs):
        # double_click(selector)
        self.double_click(*args, **kwargs)

    def ゆっくりクリックして(self, *args, **kwargs):
        # slow_click(selector)
        self.slow_click(*args, **kwargs)

    def リンクテキストをクリックします(self, *args, **kwargs):
        # click_link_text(link_text)
        self.click_link_text(*args, **kwargs)

    def テキストを更新(self, *args, **kwargs):
        # update_text(selector, new_value)
        self.update_text(*args, **kwargs)

    def テキストを追加(self, *args, **kwargs):
        # add_text(selector, new_value)
        self.add_text(*args, **kwargs)

    def テキストを取得(self, *args, **kwargs):
        # get_text(selector, new_value)
        self.get_text(*args, **kwargs)

    def テキストを確認する(self, *args, **kwargs):
        # assert_text(text, selector)
        self.assert_text(*args, **kwargs)

    def 正確なテキストを確認する(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        self.assert_exact_text(*args, **kwargs)

    def 要素を確認する(self, *args, **kwargs):
        # assert_element(selector)
        self.assert_element(*args, **kwargs)

    def タイトルを確認(self, *args, **kwargs):
        # assert_title(title)
        self.assert_title(*args, **kwargs)

    def 検証が正しい(self, *args, **kwargs):
        # assert_true(expr)
        self.assert_true(*args, **kwargs)

    def 検証は偽です(self, *args, **kwargs):
        # assert_false(expr)
        self.assert_false(*args, **kwargs)

    def 検証が等しい(self, *args, **kwargs):
        # assert_equal(first, second)
        self.assert_equal(*args, **kwargs)

    def 検証が等しくない(self, *args, **kwargs):
        # assert_not_equal(first, second)
        self.assert_not_equal(*args, **kwargs)

    def ページを更新する(self, *args, **kwargs):
        # refresh_page()
        self.refresh_page(*args, **kwargs)

    def 現在のURLを取得(self, *args, **kwargs):
        # get_current_url()
        self.get_current_url(*args, **kwargs)

    def ページのソースコードを取得する(self, *args, **kwargs):
        # get_page_source()
        self.get_page_source(*args, **kwargs)

    def 戻る(self, *args, **kwargs):
        # go_back()
        self.go_back(*args, **kwargs)

    def 進む(self, *args, **kwargs):
        # go_forward()
        self.go_forward(*args, **kwargs)

    def テキストが表示されています(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        self.is_text_visible(*args, **kwargs)

    def 要素は表示されますか(self, *args, **kwargs):
        # is_element_visible(selector)
        self.is_element_visible(*args, **kwargs)

    def 要素が存在するかどうか(self, *args, **kwargs):
        # is_element_present(selector)
        self.is_element_present(*args, **kwargs)

    def テキストを待つ(self, *args, **kwargs):
        # wait_for_text(text, selector)
        self.wait_for_text(*args, **kwargs)

    def 要素を待つ(self, *args, **kwargs):
        # wait_for_element(selector)
        self.wait_for_element(*args, **kwargs)

    def 眠る(self, *args, **kwargs):
        # sleep(seconds)
        self.sleep(*args, **kwargs)

    def を提出す(self, *args, **kwargs):
        # submit(selector)
        self.submit(*args, **kwargs)

    def JSクリックして(self, *args, **kwargs):
        # js_click(selector)
        self.js_click(*args, **kwargs)

    def htmlをチェック(self, *args, **kwargs):
        # inspect_html()
        self.inspect_html(*args, **kwargs)

    def スクリーンショットを保存(self, *args, **kwargs):
        # save_screenshot(name)
        self.save_screenshot(*args, **kwargs)

    def ファイルを選択(self, *args, **kwargs):
        # choose_file(selector, file_path)
        self.choose_file(*args, **kwargs)

    def スクリプトを実行する(self, *args, **kwargs):
        # execute_script(script)
        self.execute_script(*args, **kwargs)

    def 広告ブロック(self, *args, **kwargs):
        # ad_block()
        self.ad_block(*args, **kwargs)

    def スキップする(self, *args, **kwargs):
        # skip(reason="")
        self.skip(*args, **kwargs)

    def リンク切れを確認する(self, *args, **kwargs):
        # assert_no_404_errors()
        self.assert_no_404_errors(*args, **kwargs)

    def JSエラーを確認する(self, *args, **kwargs):
        # assert_no_js_errors()
        self.assert_no_js_errors(*args, **kwargs)

    def フレームに切り替え(self, *args, **kwargs):
        # switch_to_frame(frame)
        self.switch_to_frame(*args, **kwargs)

    def デフォルトのコンテンツに切り替える(self, *args, **kwargs):
        # switch_to_default_content()
        self.switch_to_default_content(*args, **kwargs)

    def 新しいウィンドウを開く(self, *args, **kwargs):
        # open_new_window()
        self.open_new_window(*args, **kwargs)

    def ウィンドウに切り替え(self, *args, **kwargs):
        # switch_to_window(window)
        self.switch_to_window(*args, **kwargs)

    def デフォルトのウィンドウに切り替える(self, *args, **kwargs):
        # switch_to_default_window()
        self.switch_to_default_window(*args, **kwargs)

    def ハイライト(self, *args, **kwargs):
        # highlight(selector)
        self.highlight(*args, **kwargs)

    def ハイライトしてクリックして(self, *args, **kwargs):
        # highlight_click(selector)
        self.highlight_click(*args, **kwargs)

    def スクロールして(self, *args, **kwargs):
        # scroll_to(selector)
        self.scroll_to(*args, **kwargs)

    def 一番上までスクロール(self, *args, **kwargs):
        # scroll_to_top()
        self.scroll_to_top(*args, **kwargs)

    def 一番下までスクロール(self, *args, **kwargs):
        # scroll_to_bottom()
        self.scroll_to_bottom(*args, **kwargs)
