from seleniumbase import BaseCase


class CalculatorTests(BaseCase):
    def test_6_times_7_plus_12_equals_54(self):
        self.open("seleniumbase.io/apps/calculator")
        self.click('button[id="6"]')
        self.click("button#multiply")
        self.click('button[id="7"]')
        self.click("button#add")
        self.click('button[id="1"]')
        self.click('button[id="2"]')
        self.click("button#equal")
        self.assert_exact_text("54", "input#output")
