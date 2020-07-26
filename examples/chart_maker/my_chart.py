from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):

    def test_chart_maker(self):
        self.create_pie_chart(title="Automated Tests")
        self.add_data_point("Passed", 7, color="#95d96f")
        self.add_data_point("Untested", 2, color="#eaeaea")
        self.add_data_point("Failed", 1, color="#f1888f")
        self.create_presentation()
        self.add_slide(self.extract_chart())
        self.begin_presentation()
