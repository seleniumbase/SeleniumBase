<h3 align="left"><img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb23.png" alt="SeleniumBase" width="290" /></h3>

# 📊 Chart Maker 📊

SeleniumBase Chart Maker allows you to create HTML charts with Python.<br />
The HighCharts library is used for creating charts.
(Currently only <b>pie charts</b> are supported.)

**Here's a sample chart:**

<a href="https://seleniumbase.io/other/chart_presentation.html"><img width="500" src="https://seleniumbase.io/other/sample_pie_chart.png" title="Screenshot"></a><br>

([Click on the image for the actual chart](https://seleniumbase.io/other/chart_presentation.html))

Here's how to run the example (a chart in a presentation):
```
cd examples/chart_maker
pytest my_chart.py
```


### Creating a new chart:

```python
self.create_pie_chart(chart_name=None, title="My Chart")
""" Creates a JavaScript pie chart using "HighCharts". """
```

If creating multiple charts at the same time, you can pass the ``chart_name`` parameter to distinguish between different charts.


### Adding a data point to a chart:

```python
self.add_data_point(label, value, color=None, chart_name=None):
""" Add a data point to a SeleniumBase-generated chart.
    @Params
    label - The label name for the data point.
    value - The numeric value of the data point.
    color - The HTML color of the data point.
            Can be an RGB color. Eg: "#55ACDC".
            Can also be a named color. Eg: "Teal".
    chart_name - If creating multiple charts,
                 use this to select which one.
"""
```


### Saving a chart to a file:

```python
self.save_chart(chart_name=None, filename=None):
""" Saves a SeleniumBase-generated chart to a file for later use.
    @Params
    chart_name - If creating multiple charts at the same time,
                 use this to select the one you wish to use.
    filename - The name of the HTML file that you wish to
               save the chart to. (filename must end in ".html")
"""
```

The full HTML of the chart is saved to the ``saved_charts/`` folder.


### Extracting the HTML of a chart:

```python
self.extract_chart(chart_name=None):
""" Extracts the HTML from a SeleniumBase-generated chart.
    @Params
    chart_name - If creating multiple charts at the same time,
                 use this to select the one you wish to use.
"""
```


### Displaying a chart in the browser window:

```python
self.display_chart(chart_name=None, filename=None):
""" Displays a SeleniumBase-generated chart in the browser window.
    @Params
    chart_name - If creating multiple charts at the same time,
                 use this to select the one you wish to use.
    filename - The name of the HTML file that you wish to
               save the chart to. (filename must end in ".html")
"""
```

All methods have the optional ``chart_name`` argument, which is only needed if you're creating multiple charts at once.


### Here's an example of using SeleniumBase Chart Maker:

```python
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

```

#### This example is from [my_chart.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/chart_maker/my_chart.py), which you can run from the ``examples/chart_maker`` folder with the following command:

```bash
pytest my_chart.py
```
