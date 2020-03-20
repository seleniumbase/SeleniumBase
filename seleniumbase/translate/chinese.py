# Chinese Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class 硒测试用例(BaseCase):  # noqa

    def 开启网址(self, *args, **kwargs):
        # open(url)
        self.open(*args, **kwargs)

    def 单击(self, *args, **kwargs):
        # click(selector)
        self.click(*args, **kwargs)

    def 双击(self, *args, **kwargs):
        # double_click(selector)
        self.double_click(*args, **kwargs)

    def 慢单击(self, *args, **kwargs):
        # slow_click(selector)
        self.slow_click(*args, **kwargs)

    def 单击链接文本(self, *args, **kwargs):
        # click_link_text(link_text)
        self.click_link_text(*args, **kwargs)

    def 更新文本(self, *args, **kwargs):
        # update_text(selector, new_value)
        self.update_text(*args, **kwargs)

    def 添加文本(self, *args, **kwargs):
        # add_text(selector, new_value)
        self.add_text(*args, **kwargs)

    def 获取文本(self, *args, **kwargs):
        # get_text(selector, new_value)
        self.get_text(*args, **kwargs)

    def 断言文本(self, *args, **kwargs):
        # assert_text(text, selector)
        self.assert_text(*args, **kwargs)

    def 确切断言文本(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        self.assert_exact_text(*args, **kwargs)

    def 断言元素(self, *args, **kwargs):
        # assert_element(selector)
        self.assert_element(*args, **kwargs)

    def 断言标题(self, *args, **kwargs):
        # assert_title(title)
        self.assert_title(*args, **kwargs)

    def 断言为真(self, *args, **kwargs):
        # assert_true(expr)
        self.assert_true(*args, **kwargs)

    def 断言为假(self, *args, **kwargs):
        # assert_false(expr)
        self.assert_false(*args, **kwargs)

    def 断言等于(self, *args, **kwargs):
        # assert_equal(first, second)
        self.assert_equal(*args, **kwargs)

    def 断言不等于(self, *args, **kwargs):
        # assert_not_equal(first, second)
        self.assert_not_equal(*args, **kwargs)

    def 刷新页面(self, *args, **kwargs):
        # refresh_page()
        self.refresh_page(*args, **kwargs)

    def 获取当前网址(self, *args, **kwargs):
        # get_current_url()
        self.get_current_url(*args, **kwargs)

    def 获取页面源代码(self, *args, **kwargs):
        # get_page_source()
        self.get_page_source(*args, **kwargs)

    def 回去(self, *args, **kwargs):
        # go_back()
        self.go_back(*args, **kwargs)

    def 向前(self, *args, **kwargs):
        # go_forward()
        self.go_forward(*args, **kwargs)

    def 文本是否显示(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        self.is_text_visible(*args, **kwargs)

    def 元素是否可见(self, *args, **kwargs):
        # is_element_visible(selector)
        self.is_element_visible(*args, **kwargs)

    def 元素是否存在(self, *args, **kwargs):
        # is_element_present(selector)
        self.is_element_present(*args, **kwargs)

    def 等待文本(self, *args, **kwargs):
        # wait_for_text(text, selector="html")
        self.wait_for_text(*args, **kwargs)

    def 等待元素(self, *args, **kwargs):
        # wait_for_element(selector)
        self.wait_for_element(*args, **kwargs)

    def 睡(self, *args, **kwargs):
        # sleep(seconds)
        self.sleep(*args, **kwargs)

    def 提交(self, *args, **kwargs):
        # submit(selector)
        self.submit(*args, **kwargs)

    def JS单击(self, *args, **kwargs):
        # js_click(selector)
        self.js_click(*args, **kwargs)

    def 检查HTML(self, *args, **kwargs):
        # inspect_html()
        self.inspect_html(*args, **kwargs)

    def 保存截图(self, *args, **kwargs):
        # save_screenshot(name)
        self.save_screenshot(*args, **kwargs)

    def 选择文件(self, *args, **kwargs):
        # choose_file(selector, file_path)
        self.choose_file(*args, **kwargs)

    def 执行脚本(self, *args, **kwargs):
        # execute_script(script)
        self.execute_script(*args, **kwargs)

    def 广告区块(self, *args, **kwargs):
        # ad_block()
        self.ad_block(*args, **kwargs)

    def 跳过(self, *args, **kwargs):
        # skip(reason="")
        self.skip(*args, **kwargs)

    def 检查断开的链接(self, *args, **kwargs):
        # assert_no_404_errors()
        self.assert_no_404_errors(*args, **kwargs)

    def 检查JS错误(self, *args, **kwargs):
        # assert_no_js_errors()
        self.assert_no_js_errors(*args, **kwargs)

    def 切换到帧(self, *args, **kwargs):
        # switch_to_frame(frame)
        self.switch_to_frame(*args, **kwargs)

    def 切换到默认内容(self, *args, **kwargs):
        # switch_to_default_content()
        self.switch_to_default_content(*args, **kwargs)

    def 打开新窗口(self, *args, **kwargs):
        # open_new_window()
        self.open_new_window(*args, **kwargs)

    def 切换到窗口(self, *args, **kwargs):
        # switch_to_window(window)
        self.switch_to_window(*args, **kwargs)

    def 切换到默认窗口(self, *args, **kwargs):
        # switch_to_default_window()
        self.switch_to_default_window(*args, **kwargs)

    def 亮点(self, *args, **kwargs):
        # highlight(selector)
        self.highlight(*args, **kwargs)

    def 亮点单击(self, *args, **kwargs):
        # highlight_click(selector)
        self.highlight_click(*args, **kwargs)

    def 滚动到(self, *args, **kwargs):
        # scroll_to(selector)
        self.scroll_to(*args, **kwargs)

    def 滚动到顶部(self, *args, **kwargs):
        # scroll_to_top()
        self.scroll_to_top(*args, **kwargs)

    def 滚动到底部(self, *args, **kwargs):
        # scroll_to_bottom()
        self.scroll_to_bottom(*args, **kwargs)
