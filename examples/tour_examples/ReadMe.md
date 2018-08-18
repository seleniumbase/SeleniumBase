## Creating SeleniumBase Tours

![](https://cdn2.hubspot.net/hubfs/100006/images/google_tour.gif "SeleniumBase Tours")<br>

SeleniumBase Tours utilize the [Shepherd Library](https://cdnjs.com/libraries/shepherd/1.8.1) for creating and running tours, demos, and walkthroughs on any website.

To utilize tours, there are three methods that you need to know at the basic level (which contain optional arguments):

``self.create_tour(theme)``

``self.add_tour_step(message, css_selector, title, alignment, theme)``

``self.play_tour(interval)``

With the ``create_tour()`` method, you can pass a default theme to change the look & feel of the tour steps. Valid themes are ``dark``, ``default``, ``arrows``, ``square``, and ``square-dark``.

With the ``self.add_tour_step()`` method, at minimum you must pass a message to display. Then you can specify a web element to attach to (by CSS selector). If no element is specified, the tour step will tether to the top of the screen by default. You can also add an optional title above the message to display with the tour step, as well as change the theme for that step, and even specify the alignment (which is the side of the element that you want the tour message to tether to).

Finally, you can play a tour you created by calling the ``self.play_tour()`` method. If you specify an interval, the tour will automatically walk through each step after that many seconds have passed.

### Here's an example of using SeleniumBase Tours:

```python
from seleniumbase import BaseCase

class MyTourClass(BaseCase):

    def test_google_tour(self):
        self.open('https://google.com')
        self.wait_for_element('input[title="Search"]')
        self.create_tour(theme="dark")
        self.add_tour_step(
        	"Click to begin the Google Tour!", title="SeleniumBase Tours")
        self.add_tour_step(
        	"Type in your search query here.", 'input[title="Search"]')
        self.add_tour_step(
        	"Then click here to search!", 'input[value="Google Search"]',
            alignment="bottom", theme="arrows")
        self.add_tour_step(
        	"Or click here to see the top result.",
        	'''[value="I'm Feeling Lucky"]''',
            alignment="bottom", theme="arrows")
        self.play_tour()
```

### This example was taken from [google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py), which you can run with:

```bash
pytest google_tour.py
```
