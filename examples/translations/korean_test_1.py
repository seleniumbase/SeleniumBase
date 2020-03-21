# Korean Language Test - Python 3 Only!
from seleniumbase.translate.korean import 셀레늄_테스트_케이스  # noqa


class 테스트_클래스(셀레늄_테스트_케이스):  # noqa

    def test_실시예_1(self):
        self.URL_열기("https://ko.wikipedia.org/wiki/")
        self.텍스트_확인("위키백과")
        self.요소_확인('[title="위키백과:소개"]')
        self.텍스트를_업데이트("#searchInput", "김치")
        self.클릭("#searchButton")
        self.텍스트_확인("김치", "#firstHeading")
        self.요소_확인('img[alt="Various kimchi.jpg"]')
        self.텍스트를_업데이트("#searchInput", "비빔밥")
        self.클릭("#searchButton")
        self.텍스트_확인("비빔밥", "#firstHeading")
        self.요소_확인('img[alt="Dolsot-bibimbap.jpg"]')
