# Chinese Language Test
from seleniumbase.translate.chinese import 硒测试用例  # noqa


class 我的测试类(硒测试用例):

    def test_例子1(self):
        self.开启("https://zh.wikipedia.org/wiki/")
        self.断言标题("维基百科，自由的百科全书")
        self.断言元素('a[title="首页"]')
        self.断言文本("新闻动态", "span#新闻动态")
        self.输入文本("#searchInput", "舞龍")
        self.单击("#searchButton")
        self.断言文本("舞龍", "#firstHeading")
        self.断言元素('img[src*="Chinese_draak.jpg"]')
        self.输入文本("#searchInput", "火鍋")
        self.单击("#searchButton")
        self.断言文本("火鍋", "#firstHeading")
        self.断言元素('td:contains("火鍋的各種食材")')
        self.输入文本("#searchInput", "精武英雄")
        self.单击("#searchButton")
        self.断言元素('img[src*="Fist_of_legend.jpg"]')
        self.断言文本("李连杰", 'li a[title="李连杰"]')
