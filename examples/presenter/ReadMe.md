<h3 align="left"><img src="https://seleniumbase.io/cdn/img/sb_logo_b.png" alt="SeleniumBase" width="360" /></h3>

<h1> 📰 Presenter 📑 </h1>

<p>SeleniumBase Presenter lets you use Python to generate HTML presentations from Reveal JS.</p>

<b>Here's a sample presentation:</b>

<a href="https://seleniumbase.io/other/presenter.html"><img width="500" src="https://seleniumbase.io/other/presenter.gif" title="Screenshot"></a><br>

([Click on the image/GIF for the actual presentation](https://seleniumbase.io/other/presenter.html))

([Here's the code for that presentation](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/my_presentation.py))

Slides can include HTML, code, images, and iframes.

Here's how to run the example presentation:

```bash
cd examples/presenter
pytest my_presentation.py
```

**Here's a presentation with a chart:**

<a href="https://seleniumbase.io/other/core_presentation.html"><img width="428" src="https://seleniumbase.io/other/sb_core_areas.png" title="Screenshot"></a><br>

([Click on the image/GIF for the actual presentation](https://seleniumbase.io/other/core_presentation.html))

([Here's the code for that presentation](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/core_presentation.py))

Here's how to run that example:

```bash
cd examples/presenter
pytest core_presentation.py
```


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="24" /> Creating a new presentation:</h3>

```python
self.create_presentation(name=None, theme="serif", transition="default")
""" Creates a Reveal-JS presentation that you can add slides to.
    @Params
    name - If creating multiple presentations at the same time,
           use this to specify the name of the current presentation.
    theme - Set a theme with a unique style for the presentation.
            Valid themes: "serif" (default), "sky", "white", "black",
                          "simple", "league", "moon", "night",
                          "beige", "blood", and "solarized".
    transition - Set a transition between slides.
                 Valid transitions: "none" (default), "slide", "fade",
                                    "zoom", "convex", and "concave".
"""
```

If creating multiple presentations at the same time, you can pass the ``name`` parameter to distinguish between different presentations.
Notes are disabled by default. You can enable notes by specifying:
``show_notes=True``


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="24" /> Adding a slide to a presentation:</h3>

```python
self.add_slide(content=None, image=None, code=None, iframe=None,
               content2=None, notes=None, transition=None, name=None)
""" Allows the user to add slides to a presentation.
    @Params
    content - The HTML content to display on the presentation slide.
    image - Attach an image (from a URL link) to the slide.
    code - Attach code of any programming language to the slide.
           Language-detection will be used to add syntax formatting.
    iframe - Attach an iFrame (from a URL link) to the slide.
    content2 - HTML content to display after adding an image or code.
    notes - Additional notes to include with the slide.
            ONLY SEEN if show_notes is set for the presentation.
    transition - Set a transition between slides. (overrides previous)
                 Valid transitions: "none" (default), "slide", "fade",
                                    "zoom", "convex", and "concave".
    name - If creating multiple presentations at the same time,
           use this to select the presentation to add slides to.
"""
```


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="24" /> Running a presentation:</h3>

```python
self.begin_presentation(
    filename="my_presentation.html", show_notes=False, interval=0)
""" Begin a Reveal-JS Presentation in the web browser.
    @Params
    name - If creating multiple presentations at the same time,
           use this to select the one you wish to add slides to.
    filename - The name of the HTML file that you wish to
               save the presentation to. (filename must end in ".html")
    show_notes - When set to True, the Notes feature becomes enabled,
                 which allows presenters to see notes next to slides.
    interval - The delay time between autoplaying slides. (in seconds)
               If set to 0 (default), autoplay is disabled.
"""
```

Before the presentation is run, the full HTML is saved to the ``saved_presentations/`` folder.


All methods have the optional ``name`` argument, which is only needed if you're creating multiple presentations at once.

<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="24" /> Here's an example of using SeleniumBase Presenter:</h3>

```python
from seleniumbase import BaseCase


class MyPresenterClass(BaseCase):

    def test_presenter(self):
        self.create_presentation(theme="serif")
        self.add_slide(
            '<h1>Welcome</h1><br />\n'
            '<h3>Press the <b>Right Arrow</b></h3>')
        self.add_slide(
            '<h3>SeleniumBase Presenter</h3><br />\n'
            '<img width="240" src="https://seleniumbase.io/img/logo3a.png" />'
            '<span style="margin:144px;" />'
            '<img src="https://seleniumbase.io/other/python_3d_logo.png" />'
            '<br /><br />\n<h4>Create presentations with <b>Python</b></h4>')
        self.add_slide(
            '<h3>Make slides using <b>HTML</b>:</h3><br />\n'
            '<table style="padding:10px;border:4px solid black;font-size:50;">'
            '\n<tr style="background-color:CDFFFF;">\n'
            '<th>Row ABC</th><th>Row XYZ</th></tr>\n'
            '<tr style="background-color:DCFDDC;">'
            '<td>Value ONE</td><td>Value TWO</td></tr>\n'
            '<tr style="background-color:DFDFFB;">\n'
            '<td>Value THREE</td><td>Value FOUR</td></tr>\n'
            '</table><br />\n<h4>(HTML <b>table</b> example)</h4>')
        self.add_slide(
            '<h3>Keyboard Shortcuts:</h3>\n'
            '<table style="padding:10px;border:4px solid black;font-size:30;'
            'background-color:FFFFDD;">\n'
            '<tr><th>Key</th><th>Action</th></tr>\n'
            '<tr><td><b>=></b></td><td>Next Slide (N also works)</td></tr>\n'
            '<tr><td><b><=</b></td><td>Previous Slide (P also works)</td></tr>'
            '\n<tr><td>F</td><td>Full Screen Mode</td></tr>\n'
            '<tr><td>O</td><td>Overview Mode Toggle</td></tr>\n'
            '<tr><td>esc</td><td>Exit Full Screen / Overview Mode</td></tr>\n'
            '<tr><td><b>.</b></td><td>Pause/Resume Toggle</td></tr>\n'
            '<tr><td>space</td><td>Next Slide (alternative)</td></tr></table>'
            )
        self.add_slide(
            '<h3>Add <b>images</b> to slides:</h3>',
            image="https://seleniumbase.io/other/seagulls.jpg")
        self.add_slide(
            '<h3>Add <b>code</b> to slides:</h3>',
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyTestClass(BaseCase):\n\n'
                '    def test_basics(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")\n'
                '        self.open("https://xkcd.com/353/")\n'
                '        self.assert_title("xkcd: Python")\n'
                '        self.assert_element(\'img[alt="Python"]\')\n'
                '        self.click(\'a[rel="license"]\')\n'
                '        self.assert_text("free to copy and reuse")\n'
                '        self.go_back()\n'
                '        self.click_link("About")\n'
                '        self.assert_exact_text("xkcd.com", "h2")'))
        self.add_slide(
            "<h3>Highlight <b>code</b> in slides:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                '<mark>class MyTestClass(BaseCase):</mark>\n\n'
                '    def test_basics(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")'))
        self.add_slide(
            '<h3>Add <b>iFrames</b> to slides:</h3>',
            iframe="https://seleniumbase.io/demo_page")
        self.add_slide(
            '<h3>Getting started is <b>easy</b>:</h3>',
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyPresenterClass(BaseCase):\n\n'
                '    def test_presenter(self):\n'
                '        self.create_presentation(theme="serif")\n'
                '        self.add_slide("Welcome to Presenter!")\n'
                '        self.add_slide(\n'
                '            "Add code to slides:",\n'
                '            code=(\n'
                '                "from seleniumbase import BaseCase\\n\\n"\n'
                '                "class MyPresenterClass(BaseCase):\\n\\n"\n'
                '                "    def test_presenter(self):\\n"\n'
                '                "        self.create_presentation()\\n"))\n'
                '        self.begin_presentation(\n'
                '            filename="demo.html", show_notes=True)'))
        self.add_slide(
            '<h3>Include <b>notes</b> with slides:</h3><br />',
            code=('self.add_slide("[Your HTML goes here]",\n'
                  '               code="[Your software code goes here]",\n'
                  '               content2="[Additional HTML goes here]",\n'
                  '               notes="[Attached speaker notes go here]"\n'
                  '                     "[Note A! -- Note B! -- Note C! ]")'),
            notes='<h2><ul><li>Note A!<li>Note B!<li>Note C!<li>Note D!</h2>',
            content2="<h4>(Notes can include HTML tags)</h4>")
        self.add_slide(
            '<h3>Multiple <b>themes</b> available:</h3>',
            code=(
                'self.create_presentation(theme="serif")\n\n'
                'self.create_presentation(theme="sky")\n\n'
                'self.create_presentation(theme="simple")\n\n'
                'self.create_presentation(theme="white")\n\n'
                'self.create_presentation(theme="moon")\n\n'
                'self.create_presentation(theme="black")\n\n'
                'self.create_presentation(theme="night")\n\n'
                'self.create_presentation(theme="beige")\n\n'
                'self.create_presentation(theme="league")'))
        self.add_slide(
            '<h2><b>The End</b></h2>',
            image="https://seleniumbase.io/img/sb_logo_10.png")
        self.begin_presentation(
            filename="presenter.html", show_notes=True, interval=0)
```

That example is from [my_presentation.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/my_presentation.py), which you can run from the ``examples/presenter`` folder with the following command:

```bash
pytest my_presentation.py
```

<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="24" /> Saving a presentation:</h3>

If you want to save the presentation you created as an HTML file, use:

```python
self.save_presentation(filename="my_presentation.html", show_notes=True)
```

Presentations automatically get saved when calling:
```python
self.begin_presentation(show_notes=True)
```
