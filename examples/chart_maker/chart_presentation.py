from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ChartMakerPresentation(BaseCase):
    def test_chart_maker_presentation(self):
        self.create_presentation(theme="sky", transition="zoom")

        self.create_pie_chart(title="Automated Tests")
        self.add_data_point("Passed", 7, color="#95d96f")
        self.add_data_point("Untested", 2, color="#eaeaea")
        self.add_data_point("Failed", 1, color="#f1888f")
        self.add_slide("<p>Pie Chart</p>" + self.extract_chart())

        self.create_bar_chart(title="Language", legend=False)
        self.add_data_point("Python", 33, color="Orange")
        self.add_data_point("JavaScript", 27, color="Teal")
        self.add_data_point("HTML + CSS", 21, color="Purple")
        self.add_slide("<p>Bar Chart</p>" + self.extract_chart())

        self.create_column_chart(title="Colors", legend=False)
        self.add_data_point("Red", 10, color="Red")
        self.add_data_point("Green", 25, color="Green")
        self.add_data_point("Blue", 15, color="Blue")
        self.add_slide("<p>Column Chart</p>" + self.extract_chart())

        self.create_line_chart(title="Last Week's Data")
        self.add_data_point("Sun", 5)
        self.add_data_point("Mon", 10)
        self.add_data_point("Tue", 20)
        self.add_data_point("Wed", 40)
        self.add_data_point("Thu", 80)
        self.add_data_point("Fri", 65)
        self.add_data_point("Sat", 50)
        self.add_slide("<p>Line Chart</p>" + self.extract_chart())

        self.begin_presentation(filename="chart_presentation.html")
