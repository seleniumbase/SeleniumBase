from seleniumbase import BaseCase


class PieCharts(BaseCase):

    def test_pie_charts(self):
        self.create_presentation(theme="serif", transition="convex")

        self.create_pie_chart(labels=False)
        self.add_data_point("Meringue Cream", 3, color="#f1eeea")
        self.add_data_point("Lemon Filling", 3, color="#e9d655")
        self.add_data_point("Graham Cracker Crust", 1, color="#9d5b34")
        self.add_slide("<p>Lemon Meringue Pie</p>" + self.extract_chart())

        self.create_pie_chart(labels=False)
        self.add_data_point("Blueberries", 1, color="#5c81b7")
        self.add_data_point("Blueberry Filling", 2, color="#12405e")
        self.add_data_point("Golden Brown Crust", 1, color="#cd7b54")
        self.add_slide("<p>Blueberry Pie</p>" + self.extract_chart())

        self.create_pie_chart(labels=False)
        self.add_data_point("Strawberries", 1, color="#ff282c")
        self.add_data_point("Kiwis", 1, color="#a9c208")
        self.add_data_point("Apricots", 1, color="#f47a14")
        self.add_data_point("Raspberries", 1, color="#b10019")
        self.add_data_point("Black Berries", 1, color="#44001e")
        self.add_data_point("Blueberries", 1, color="#5c81b7")
        self.add_data_point("Custard", 3, color="#eee896")
        self.add_data_point("Golden Crust", 4, color="#dca422")
        self.add_slide("<p>Fruit Tart Pie</p>" + self.extract_chart())

        self.create_pie_chart(labels=False)
        self.add_data_point("Apple Crust", 4, color="#b66327")
        self.add_data_point("Apple Filling", 5, color="#c5903e")
        self.add_data_point("Cinnamon", 1, color="#76210d")
        self.add_data_point("Whipped Cream", 2, color="#f2f2f2")
        self.add_slide("<p>Apple Pie</p>" + self.extract_chart())

        self.create_pie_chart(labels=False)
        self.add_data_point("Sponge Cake", 4, color="#e0d5a0")
        self.add_data_point("Custard", 3, color="#eee896")
        self.add_data_point("Chocolate", 1, color="#5c3625")
        self.add_slide("<p>Boston Cream Pie</p>" + self.extract_chart())

        self.begin_presentation(filename="pie_charts.html")
