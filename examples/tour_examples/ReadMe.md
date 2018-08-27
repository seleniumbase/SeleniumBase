## Creating SeleniumBase Tours

SeleniumBase Tours utilize the **[Shepherd Javascript Library](https://cdnjs.com/libraries/shepherd/1.8.1)** and the **[Bootstrap Tour Library](https://cdnjs.com/libraries/bootstrap-tour)** for creating and running tours, demos, and walkthroughs on any website.

Example tour utilizing the Shepherd Javascript Library:

<img src="https://cdn2.hubspot.net/hubfs/100006/images/google_tour.gif" title="Shepherd Tour" height="348"><br>

Example tour utilizing the Bootstrap Javascript Library:

<img src="https://cdn2.hubspot.net/hubfs/100006/images/google_tour_2.gif" title="Bootstrap Tour" height="340"><br>

By default, the Shepherd Javascript Library is used when creating a tour with:

``self.create_tour()``

To create a tour utilizing the Bootstrap Javascript Library, you can use either of the following:

``self.create_bootstrap_tour()``

OR

``self.create_tour(theme="bootstrap")``

To add a tour step, use the following: (Only ``message`` is required. The other args are optional.)

``self.add_tour_step(message, css_selector, title, alignment, theme)``

Here's how you play a tour:

``self.play_tour(interval)``

With the ``create_tour()`` method, you can pass a default theme to change the look & feel of the tour steps. Valid themes are ``dark``, ``default``, ``arrows``, ``square``, and ``square-dark``.

With the ``self.add_tour_step()`` method, you must first pass a message to display. You can then specify a web element to attach to (by using [CSS selectors](https://www.w3schools.com/cssref/css_selectors.asp)). If no element is specified, the tour step will tether to the top of the screen by default. You can also add an optional title above the message to display with the tour step, as well as change the theme for that step, and even specify the alignment (which is the side of the element that you want the tour message to tether to).

Finally, you can play a tour you created by calling the ``self.play_tour()`` method. If you specify an interval, the tour will automatically walk through each step after that many seconds have passed.

All methods have the optional ``name`` argument, which is only needed if you're creating multiple tours at once. Then, when you're adding a step or playing a tour, SeleniumBase knows which tour you're referring too. You can avoid using the ``name`` arg for multiple tours if you play a tour before creating a new one.

### Here's an example of using SeleniumBase Tours:

```python
from seleniumbase import BaseCase

class MyTourClass(BaseCase):

    def test_google_tour(self):
        self.open('https://google.com')
        self.wait_for_element('input[title="Search"]')

        self.create_tour(theme="dark")
        self.add_tour_step("Click to begin the Google Tour!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your search query here.", 'input[title="Search"]')
        self.add_tour_step("Then click here to search!", 'input[value="Google Search"]',
            alignment="bottom", theme="arrows")
        self.add_tour_step("Or click here to see the top result.",
            '''[value="I'm Feeling Lucky"]''', alignment="bottom", theme="arrows")
        self.play_tour()
```

#### This example was taken from [google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py), which you can run from the ``examples/tour_examples`` folder with the following command:

```bash
pytest google_tour.py
```

#### There's also the Bootstrap Google Tour, which you can play with the following command:

```bash
pytest bootstrap_google_tour.py
```
