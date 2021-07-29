# -*- coding: utf-8 -*-
from seleniumbase import BaseCase


class ChinesePdfTests(BaseCase):
    def test_chinese_pdf(self):

        pdf = (
            "https://github.com/seleniumbase/SeleniumBase/"
            "files/3895614/unittest.pdf"
        )

        # Get and print PDF text
        pdf_text = self.get_pdf_text(pdf, page=2)
        self._print("\n" + pdf_text)

        # Assert PDF contains the expected text on Page 2
        self.assert_pdf_text(pdf, "个测试类", page=2)

        # Assert PDF contains the expected text on any of the pages
        self.assert_pdf_text(pdf, "运行单元测试")
        self.assert_pdf_text(pdf, "等待测试结束后显示所有结果")
        self.assert_pdf_text(pdf, "测试的执行跟方法的顺序没有关系")
