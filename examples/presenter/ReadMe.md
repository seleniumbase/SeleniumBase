<h3 align="left"><img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb23.png" alt="SeleniumBase" width="290" /></h3>

# 📰 Presenter 📰

SeleniumBase Presenter allows you to create an HTML presentation with only a few lines of Python.
The Reveal-JS library is used for running the presentations.

**Here's a sample slide:**

<img src="https://seleniumbase.io/other/presenter_screen.png" title="Screenshot"><br>

Slides can include HTML, code, images, and iframes.

Here's how to run the example presentation:
```
cd examples/presenter
pytest my_presentation.py
```


### Creating a new presentation:

```python
self.create_presentation(name=None, show_notes=True)
        """ Creates a Reveal-JS presentation that you can add slides to.
            @Params
            name - If creating multiple presentations at the same time,
                   use this to specify the name of the current presentation.
            show_notes - When set to True, the Notes feature becomes enabled,
                         which allows presenters to see notes next to slides.
        """
```

If creating multiple presentations at the same time, you can pass the ``name`` parameter to distinguish between different presentations.
Notes are enabled by default unless you specify:
``show_notes=False`` when calling.


### Adding a slide to a presentation:

```python
self.add_slide(content=None, image=None, code=None, iframe=None,
               notes=None, name=None)
        """ Allows the user to add slides to a presentation.
            @Params
            content - The HTML content to display on the presentation slide.
            image - Attach an image (from a URL link) to the slide.
            code - Attach code of any programming language to the slide.
                   Language-detection will be used to add syntax formatting.
            iframe - Attach an iFrame (from a URL link) to the slide.
            notes - Additional notes to include with the slide.
                    ONLY SEEN if show_notes is set for the presentation.
            name - If creating multiple presentations at the same time,
                   use this to select the presentation to add slides to.
        """
```


### Running a presentation:

```python
self.begin_presentation(filename="my_presentation.html", name=None)
        """ Begin a Reveal-JS Presentation in the web browser. """
```

Before the presentation is run, the full HTML is saved to the ``presentations_saved/`` folder.


All methods have the optional ``name`` argument, which is only needed if you're creating multiple presentations at once.

### Here's an example of using SeleniumBase Presenter:

```python
from seleniumbase import BaseCase


class MyPresenterClass(BaseCase):

    def test_presenter(self):
        self.create_presentation()
        self.add_slide(
            "<h2>Welcome!</h2>"
            "<h4>Enjoy the Presentation!</h4>")
        self.add_slide(
            '<h3>SeleniumBase "Presenter"</h3>'
            '<img src="https://seleniumbase.io/img/logo3a.png"></img>'
            '<h4>A tool for creating presentations</h4>')
        self.add_slide(
            '<h3>You can add HTML to any slide:</h3><br />'
            '<table style="padding:10px;border:4px solid black;font-size:60;">'
            '<tr><th>Row 1</th><th>Row 2</th></tr>'
            '<tr><td>Value 1</td><td>Value 2</td></tr></table><br />'
            '<h4>(HTML table example)</h4>')
        self.add_slide(
            "<h3>You can display code:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyTestClass(BaseCase):\n\n'
                '    def test_basic(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")\n'
                '        self.open("https://xkcd.com/353/")\n'
                '        self.assert_title("xkcd: Python")\n'
                '        self.assert_element(\'img[alt="Python"]\')\n'
                '        self.click(\'a[rel="license"]\')\n'
                '        self.assert_text("free to copy and reuse")\n'
                '        self.go_back()\n'
                '        self.click_link_text("About")\n'
                '        self.assert_exact_text("xkcd.com", "h2")\n'))
        self.add_slide(
            "<h3>You can highlight code:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                '<mark>class MyTestClass(BaseCase):</mark>\n\n'
                '    def test_basic(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'))
        self.add_slide(
            "<h3>You can add notes to slides:</h3>",
            notes="<h2><ul><li>Note A!<li>Note B!<li>Note C!<li>Note D!</h2>")
        self.add_slide(
            "<h3>You can add images to slides:</h3>",
            image="https://seleniumbase.io/img/sb_logo_10.png")
        self.add_slide(
            "<h3>You can add iframes to slides:</h3>",
            iframe="https://seleniumbase.io/demo_page")
        self.add_slide("<h1>The End</h1>")
        self.begin_presentation()
```

#### This example is from [my_presentation.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/my_presentation.py), which you can run from the ``examples/presenter`` folder with the following command:

```bash
pytest my_presentation.py
```

### Saving a presentation:

If you want to save the presentation you created as an HTML file, use:

```python
self.save_presentation(filename="my_presentation.html", name=None)
```

Presentations automatically get saved when calling:
```python
self.begin_presentation()
```
