# Chinese Language Translations - Python 3 Only!
from seleniumbase import BaseCase


class 硒测试用例(BaseCase):  # noqa

    def 开启网址(self, *args, **kwargs):
        # open(url)
        return self.open(*args, **kwargs)

    def 单击(self, *args, **kwargs):
        # click(selector)
        return self.click(*args, **kwargs)

    def 双击(self, *args, **kwargs):
        # double_click(selector)
        return self.double_click(*args, **kwargs)

    def 慢单击(self, *args, **kwargs):
        # slow_click(selector)
        return self.slow_click(*args, **kwargs)

    def 单击链接文本(self, *args, **kwargs):
        # click_link_text(link_text)
        return self.click_link_text(*args, **kwargs)

    def 更新文本(self, *args, **kwargs):
        # update_text(selector, new_value)
        return self.update_text(*args, **kwargs)

    def 添加文本(self, *args, **kwargs):
        # add_text(selector, new_value)
        return self.add_text(*args, **kwargs)

    def 获取文本(self, *args, **kwargs):
        # get_text(selector, new_value)
        return self.get_text(*args, **kwargs)

    def 断言文本(self, *args, **kwargs):
        # assert_text(text, selector)
        return self.assert_text(*args, **kwargs)

    def 确切断言文本(self, *args, **kwargs):
        # assert_exact_text(text, selector)
        return self.assert_exact_text(*args, **kwargs)

    def 断言元素(self, *args, **kwargs):
        # assert_element(selector)
        return self.assert_element(*args, **kwargs)

    def 断言标题(self, *args, **kwargs):
        # assert_title(title)
        return self.assert_title(*args, **kwargs)

    def 断言为真(self, *args, **kwargs):
        # assert_true(expr)
        return self.assert_true(*args, **kwargs)

    def 断言为假(self, *args, **kwargs):
        # assert_false(expr)
        return self.assert_false(*args, **kwargs)

    def 断言等于(self, *args, **kwargs):
        # assert_equal(first, second)
        return self.assert_equal(*args, **kwargs)

    def 断言不等于(self, *args, **kwargs):
        # assert_not_equal(first, second)
        return self.assert_not_equal(*args, **kwargs)

    def 刷新页面(self, *args, **kwargs):
        # refresh_page()
        return self.refresh_page(*args, **kwargs)

    def 获取当前网址(self, *args, **kwargs):
        # get_current_url()
        return self.get_current_url(*args, **kwargs)

    def 获取页面源代码(self, *args, **kwargs):
        # get_page_source()
        return self.get_page_source(*args, **kwargs)

    def 回去(self, *args, **kwargs):
        # go_back()
        return self.go_back(*args, **kwargs)

    def 向前(self, *args, **kwargs):
        # go_forward()
        return self.go_forward(*args, **kwargs)

    def 文本是否显示(self, *args, **kwargs):
        # is_text_visible(text, selector="html")
        return self.is_text_visible(*args, **kwargs)

    def 元素是否可见(self, *args, **kwargs):
        # is_element_visible(selector)
        return self.is_element_visible(*args, **kwargs)

    def 元素是否存在(self, *args, **kwargs):
        # is_element_present(selector)
        return self.is_element_present(*args, **kwargs)

    def 等待文本(self, *args, **kwargs):
        # wait_for_text(text, selector="html")
        return self.wait_for_text(*args, **kwargs)

    def 等待元素(self, *args, **kwargs):
        # wait_for_element(selector)
        return self.wait_for_element(*args, **kwargs)

    def 睡(self, *args, **kwargs):
        # sleep(seconds)
        return self.sleep(*args, **kwargs)

    def 提交(self, *args, **kwargs):
        # submit(selector)
        return self.submit(*args, **kwargs)

    def JS单击(self, *args, **kwargs):
        # js_click(selector)
        return self.js_click(*args, **kwargs)

    def 检查HTML(self, *args, **kwargs):
        # inspect_html()
        return self.inspect_html(*args, **kwargs)

    def 保存截图(self, *args, **kwargs):
        # save_screenshot(name)
        return self.save_screenshot(*args, **kwargs)

    def 选择文件(self, *args, **kwargs):
        # choose_file(selector, file_path)
        return self.choose_file(*args, **kwargs)

    def 执行脚本(self, *args, **kwargs):
        # execute_script(script)
        return self.execute_script(*args, **kwargs)

    def 广告区块(self, *args, **kwargs):
        # ad_block()
        return self.ad_block(*args, **kwargs)

    def 跳过(self, *args, **kwargs):
        # skip(reason="")
        return self.skip(*args, **kwargs)

    def 检查断开的链接(self, *args, **kwargs):
        # assert_no_404_errors()
        return self.assert_no_404_errors(*args, **kwargs)

    def 检查JS错误(self, *args, **kwargs):
        # assert_no_js_errors()
        return self.assert_no_js_errors(*args, **kwargs)

    def 切换到帧(self, *args, **kwargs):
        # switch_to_frame(frame)
        return self.switch_to_frame(*args, **kwargs)

    def 切换到默认内容(self, *args, **kwargs):
        # switch_to_default_content()
        return self.switch_to_default_content(*args, **kwargs)

    def 打开新窗口(self, *args, **kwargs):
        # open_new_window()
        return self.open_new_window(*args, **kwargs)

    def 切换到窗口(self, *args, **kwargs):
        # switch_to_window(window)
        return self.switch_to_window(*args, **kwargs)

    def 切换到默认窗口(self, *args, **kwargs):
        # switch_to_default_window()
        return self.switch_to_default_window(*args, **kwargs)

    def 亮点(self, *args, **kwargs):
        # highlight(selector)
        return self.highlight(*args, **kwargs)

    def 亮点单击(self, *args, **kwargs):
        # highlight_click(selector)
        return self.highlight_click(*args, **kwargs)

    def 滚动到(self, *args, **kwargs):
        # scroll_to(selector)
        return self.scroll_to(*args, **kwargs)

    def 滚动到顶部(self, *args, **kwargs):
        # scroll_to_top()
        return self.scroll_to_top(*args, **kwargs)

    def 滚动到底部(self, *args, **kwargs):
        # scroll_to_bottom()
        return self.scroll_to_bottom(*args, **kwargs)
