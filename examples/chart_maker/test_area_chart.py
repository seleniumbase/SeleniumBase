from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):

    def test_chart_maker(self):
        self.create_presentation(theme="moon")
        self.create_area_chart(
            title="Time Outside", subtitle="Last Week", unit="Minutes")
        self.add_data_point("Sun", 5)
        self.add_data_point("Mon", 10)
        self.add_data_point("Tue", 20)
        self.add_data_point("Wed", 40)
        self.add_data_point("Thu", 80)
        self.add_data_point("Fri", 65)
        self.add_data_point("Sat", 50)
        self.add_slide("<p><b>Area Chart</b></p>" + self.extract_chart())
        self.begin_presentation(filename="line_chart.html", interval=8)
