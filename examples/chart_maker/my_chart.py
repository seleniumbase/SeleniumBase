from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):

    def test_chart_maker(self):
        self.create_presentation()

        self.create_pie_chart(title="Automated Tests")
        self.add_data_point("Passed", 7, color="#95d96f")
        self.add_data_point("Untested", 2, color="#eaeaea")
        self.add_data_point("Failed", 1, color="#f1888f")
        self.add_slide(self.extract_chart())

        self.create_bar_chart(title="Code", libs=False)
        self.add_data_point("Python", 33, color="Orange")
        self.add_data_point("JavaScript", 27, color="Teal")
        self.add_data_point("HTML + CSS", 21, color="Purple")
        self.add_slide(self.extract_chart())

        self.create_column_chart(title="Colors", libs=False)
        self.add_data_point("Red", 10, color="Red")
        self.add_data_point("Green", 25, color="Green")
        self.add_data_point("Blue", 15, color="Blue")
        self.add_slide(self.extract_chart())

        self.begin_presentation()
