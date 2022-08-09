# Japanese Language Test
from seleniumbase.translate.japanese import セレニウムテストケース  # noqa


class 私のテストクラス(セレニウムテストケース):
    def test_例1(self):
        self.を開く("https://ja.wikipedia.org/wiki/")
        self.テキストを確認する("ウィキペディア")
        self.要素を確認する('[title*="ウィキペディアへようこそ"]')
        self.JS入力('input[name="search"]', "アニメ")
        self.クリックして("#searchform button")
        self.テキストを確認する("アニメ", "#firstHeading")
        self.JS入力('input[name="search"]', "寿司")
        self.クリックして("#searchform button")
        self.テキストを確認する("寿司", "#firstHeading")
        self.要素を確認する('img[alt="握り寿司"]')
        self.JS入力("#searchInput", "レゴランド・ジャパン")
        self.クリックして("#searchform button")
        self.要素を確認する('img[alt*="LEGOLAND JAPAN"]')
        self.リンクテキストを確認する("名古屋城")
        self.リンクテキストをクリックします("テーマパーク")
        self.テキストを確認する("テーマパーク", "#firstHeading")
