from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):

    def test_display_chart(self):
        self.create_pie_chart(title="Pie Chart")
        self.add_data_point("Passed", 7, color="#95d96f")
        self.add_data_point("Untested", 2, color="#eaeaea")
        self.add_data_point("Failed", 1, color="#f1888f")
        self.display_chart(filename="pie_chart.html", interval=2.5)

        self.create_bar_chart(title="Bar Chart")
        self.add_data_point("Python", 33, color="Orange")
        self.add_data_point("JavaScript", 27, color="Teal")
        self.add_data_point("HTML + CSS", 21, color="Purple")
        self.display_chart(filename="bar_chart.html", interval=2.5)

        self.create_column_chart(title="Column Chart")
        self.add_data_point("Red", 10, color="Red")
        self.add_data_point("Green", 25, color="Green")
        self.add_data_point("Blue", 15, color="Blue")
        self.display_chart(filename="column_chart.html", interval=2.5)

        self.create_line_chart(title="Line Chart")
        self.add_data_point("Sun", 5)
        self.add_data_point("Mon", 10)
        self.add_data_point("Tue", 20)
        self.add_data_point("Wed", 40)
        self.add_data_point("Thu", 80)
        self.add_data_point("Fri", 65)
        self.add_data_point("Sat", 50)
        self.display_chart(filename="line_chart.html", interval=2.5)
