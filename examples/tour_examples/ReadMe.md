## SeleniumBase Website Tours

SeleniumBase Tours utilize the following three Javascript libraries for creating and running tours, demos, and walkthroughs on any website: **[Shepherd JS](https://cdnjs.com/libraries/shepherd/1.8.1)**, **[Bootstrap Tour JS](https://cdnjs.com/libraries/bootstrap-tour)**, and **[Intro JS](https://cdnjs.com/libraries/intro.js)**.

Example tour:

<img src="https://cdn2.hubspot.net/hubfs/100006/google_tour_3.gif" title="SeleniumBase Tour of Google" height="310"><br>


### Creating a new tour:

By default, Shepherd JS is used when creating a tour with:

``self.create_tour()``

You can also do:

``self.create_shepherd_tour()``

With the ``create_tour()`` and ``create_shepherd_tour()`` methods, you can pass a default theme to change the look & feel of the tour steps. Valid themes for Shepherd Tours are ``dark``, ``light`` / ``arrows``, ``default``, ``square``, and ``square-dark``.

To create a tour utilizing the Bootstrap Tour Library, you can use either of the following:

``self.create_bootstrap_tour()``

OR

``self.create_tour(theme="bootstrap")``

To create a tour utilizing the Intro JS Library, you can use either of the following:

``self.create_introjs_tour()``

OR

``self.create_tour(theme="introjs")``


### Adding a step to a tour:

To add a tour step, use the following: (Only ``message`` is required. The other args are optional.)

``self.add_tour_step(message, css_selector, title, alignment, theme)``

With the ``self.add_tour_step()`` method, you must first pass a message to display. You can then specify a web element to attach to (by using [CSS selectors](https://www.w3schools.com/cssref/css_selectors.asp)). If no element is specified, the tour step will tether to the top of the screen by default. You can also add an optional title above the message to display with the tour step, as well as change the theme for that step (Shepherd tours only), and even specify the alignment (which is the side of the element that you want the tour message to tether to).


### Playing a tour:

You can play a tour by calling:

``self.play_tour(interval)``

 If you specify an interval (optional), the tour will automatically walk through each step after that many seconds have passed.


All methods have the optional ``name`` argument, which is only needed if you're creating multiple tours at once. Then, when you're adding a step or playing a tour, SeleniumBase knows which tour you're referring too. You can avoid using the ``name`` arg for multiple tours if you play a tour before creating a new one.

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
        self.play_tour()

        self.highlight_update_text('input[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        self.create_tour(theme="light")
        self.add_tour_step(
            "Then click here to search.", 'input[value="Google Search"]')
        self.add_tour_step(
            "Or press [ENTER] after typing a query here.", '[title="Search"]')
        self.play_tour()
```

#### This example was taken from [google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py), which you can run from the ``examples/tour_examples`` folder with the following command:

```bash
pytest google_tour.py
```
