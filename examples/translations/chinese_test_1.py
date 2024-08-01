# Chinese Language Test
from seleniumbase.translate.chinese import 硒测试用例
硒测试用例.main(__name__, __file__)


class 我的测试类(硒测试用例):
    def test_例子1(self):
        self.开启("https://zh.wikipedia.org/wiki/")
        self.断言标题("维基百科，自由的百科全书")
        self.断言元素('a[title="Wikipedia:关于"]')
        self.如果可见请单击('button[aria-label="关闭"]')
        self.如果可见请单击('button[aria-label="關閉"]')
        self.断言元素('span:contains("创建账号")')
        self.断言元素('span:contains("登录")')
        self.输入文本('input[name="search"]', "舞龍")
        self.单击('button:contains("搜索")')
        self.断言文本("舞龍", "#firstHeading")
        self.断言元素('img[src*="Chinese_draak.jpg"]')
        self.回去()
        self.输入文本('input[name="search"]', "麻婆豆腐")
        self.单击('button:contains("搜索")')
        self.断言文本("麻婆豆腐", "#firstHeading")
        self.断言元素('figure:contains("一家中餐館的麻婆豆腐")')
        self.回去()
        self.输入文本('input[name="search"]', "精武英雄")
        self.单击('button:contains("搜索")')
        self.断言元素('img[src*="Fist_of_legend.jpg"]')
        self.断言文本("李连杰", 'li a[title="李连杰"]')
