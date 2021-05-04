# Korean Language Test
from seleniumbase.translate.korean import 셀레늄_테스트_케이스  # noqa


class 테스트_클래스(셀레늄_테스트_케이스):
    def test_실시예_1(self):
        self.열기("https://ko.wikipedia.org/wiki/")
        self.텍스트_확인("위키백과")
        self.요소_확인('[title="위키백과:소개"]')
        self.JS_입력("#searchform input", "김치")
        self.클릭("#searchform button")
        self.텍스트_확인("김치", "#firstHeading")
        self.요소_확인('img[alt="Various kimchi.jpg"]')
        self.링크_텍스트_확인("한국 요리")
        self.JS_입력("#searchform input", "비빔밥")
        self.클릭("#searchform button")
        self.텍스트_확인("비빔밥", "#firstHeading")
        self.요소_확인('img[alt="Dolsot-bibimbap.jpg"]')
        self.링크_텍스트를_클릭합니다("돌솥비빔밥")
        self.텍스트_확인("돌솥비빔밥", "#firstHeading")
