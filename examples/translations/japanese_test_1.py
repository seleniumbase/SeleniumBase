# Japanese Language Test
from seleniumbase.translate.japanese import セレニウムテストケース  # noqa


class 私のテストクラス(セレニウムテストケース):

    def test_例1(self):
        self.を開く("https://ja.wikipedia.org/wiki/")
        self.テキストを確認する("ウィキペディア")
        self.要素を確認する('[title="メインページに移動する"]')
        self.入力("#searchInput", "アニメ")
        self.クリックして("#searchButton")
        self.テキストを確認する("アニメ", "#firstHeading")
        self.入力("#searchInput", "寿司")
        self.クリックして("#searchButton")
        self.テキストを確認する("寿司", "#firstHeading")
        self.要素を確認する('img[alt="握り寿司"]')
        self.入力("#searchInput", "レゴランド・ジャパン")
        self.クリックして("#searchButton")
        self.要素を確認する('img[alt="Legoland japan.jpg"]')
        self.リンクテキストを確認する("名古屋城")
        self.リンクテキストをクリックします("テーマパーク")
        self.テキストを確認する("テーマパーク", "#firstHeading")
