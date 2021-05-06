from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):
    def test_multi_series(self):
        self.create_presentation(theme="league")

        self.create_line_chart(
            title="Fruit Sold Last Week", data_name="Apples", unit="Count"
        )
        self.add_data_point("Sun", 33)
        self.add_data_point("Mon", 16)
        self.add_data_point("Tue", 19)
        self.add_data_point("Wed", 28)
        self.add_data_point("Thu", 20)
        self.add_data_point("Fri", 30)
        self.add_data_point("Sat", 36)

        self.add_series_to_chart(data_name="Oranges")
        self.add_data_point("Sun", 22)
        self.add_data_point("Mon", 27)
        self.add_data_point("Tue", 23)
        self.add_data_point("Wed", 21)
        self.add_data_point("Thu", 26)
        self.add_data_point("Fri", 17)
        self.add_data_point("Sat", 25)

        self.add_series_to_chart(data_name="Strawberries")
        self.add_data_point("Sun", 41)
        self.add_data_point("Mon", 32)
        self.add_data_point("Tue", 38)
        self.add_data_point("Wed", 33)
        self.add_data_point("Thu", 31)
        self.add_data_point("Fri", 42)
        self.add_data_point("Sat", 40)

        self.add_series_to_chart(data_name="Cherries")
        self.add_data_point("Sun", 28)
        self.add_data_point("Mon", 37)
        self.add_data_point("Tue", 29)
        self.add_data_point("Wed", 24)
        self.add_data_point("Thu", 34)
        self.add_data_point("Fri", 26)
        self.add_data_point("Sat", 31)

        self.add_slide("<p>Multi-Series Line Chart</p>" + self.extract_chart())
        self.begin_presentation(filename="multi_series_chart.html", interval=8)
