<h3 align="left"><img src="https://seleniumbase.io/cdn/img/sb_logo_b.png" alt="SeleniumBase" width="320" /></h3>

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> 🛂 Dialog Boxes 🛂</h2>

SeleniumBase Dialog Boxes let your users provide input in the middle of automation scripts.

* This feature utilizes the [jquery-confirm](https://craftpip.github.io/jquery-confirm/) library.
* A Python API is used to call the JavaScript API.

<img src="https://seleniumbase.io/cdn/img/emoji_sports_dialog.png" alt="SeleniumBase" width="400" />

<h4>↕️ (<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/dialog_boxes/dialog_box_tour.py">Example: dialog_box_tour.py</a>) ↕️</h4>

<img src="https://seleniumbase.io/cdn/gif/sports_dialog.gif" alt="SeleniumBase" width="400" />

<h4>Here's how to run that example:</h4>

```bash
cd examples/dialog_boxes
pytest test_dialog_boxes.py
```

<h4>Here's a code snippet from that:</h4>

```python
self.open("https://xkcd.com/1920/")
skip_button = ["SKIP", "red"]  # Can be a [text, color] list or tuple.
buttons = ["Fencing", "Football", "Metaball", "Go/Chess", skip_button]
message = "Choose a sport:"
choice = self.get_jqc_button_input(message, buttons)
if choice == "Fencing":
    self.open("https://xkcd.com/1424/")
```

* You can create forms that include buttons and input fields.

<h4>Here's a simple form with only buttons as input:</h4>

```python
choice = self.get_jqc_button_input("Ready?", ["YES", "NO"])
print(choice)  # This prints "YES" or "NO"

# You may want to customize the color of buttons:
buttons = [("YES", "green"), ("NO", "red")]
choice = self.get_jqc_button_input("Ready?", buttons)
```

<h4>Here's a simple form with an input field:</h4>

```python
text = self.get_jqc_text_input("Enter text:", ["Search"])
print(text)  # This prints the text entered
```

<h4>This form has an input field and buttons:</h4>

```python
message = "Type your name and choose a language:"
buttons = ["Python", "JavaScript"]
text, choice = self.get_jqc_form_inputs(message, buttons)
print("Your name is: %s" % text)
print("You picked %s!" % choice)
```

<h4>You can customize options if you want:</h4>

```python
# Themes: bootstrap, modern, material, supervan, light, dark, seamless
options = [("theme", "modern"), ("width", "50%")]
self.get_jqc_text_input("You Won!", ["OK"], options)
```

<h4>Default options can be set with <code>set_jqc_theme()</code>:</h4>

```python
self.set_jqc_theme("light", color="green", width="38%")

# To reset jqc theme settings to factory defaults:
self.reset_jqc_theme()
```

<h3>All methods for Dialog Boxes:</h3>

```python
self.get_jqc_button_input(message, buttons, options=None)

self.get_jqc_text_input(message, button=None, options=None)

self.get_jqc_form_inputs(message, buttons, options=None)

self.set_jqc_theme(theme, color=None, width=None)

self.reset_jqc_theme()

self.activate_jquery_confirm()  # Automatic for jqc methods
```

<h3>Detailed method summaries for Dialog Boxes:</h3>

```python
self.get_jqc_button_input(message, buttons, options=None)
"""
Pop up a jquery-confirm box and return the text of the button clicked.
If running in headless mode, the last button text is returned.
@Params
message: The message to display in the jquery-confirm dialog.
buttons: A list of tuples for text and color.
    Example: [("Yes!", "green"), ("No!", "red")]
    Available colors: blue, green, red, orange, purple, default, dark.
    A simple text string also works: "My Button". (Uses default color.)
options: A list of tuples for options to set.
    Example: [("theme", "bootstrap"), ("width", "450px")]
    Available theme options: bootstrap, modern, material, supervan,
                             light, dark, and seamless.
    Available colors: (For the BORDER color, NOT the button color.)
        "blue", "default", "green", "red", "purple", "orange", "dark".
    Example option for changing the border color: ("color", "default")
    Width can be set using percent or pixels. Eg: "36.0%", "450px".
"""

self.get_jqc_text_input(message, button=None, options=None)
"""
Pop up a jquery-confirm box and return the text submitted by the input.
If running in headless mode, the text returned is "" by default.
@Params
message: The message to display in the jquery-confirm dialog.
button: A 2-item list or tuple for text and color. Or just the text.
    Example: ["Submit", "blue"] -> (default button if not specified)
    Available colors: blue, green, red, orange, purple, default, dark.
    A simple text string also works: "My Button". (Uses default color.)
options: A list of tuples for options to set.
    Example: [("theme", "bootstrap"), ("width", "450px")]
    Available theme options: bootstrap, modern, material, supervan,
                             light, dark, and seamless.
    Available colors: (For the BORDER color, NOT the button color.)
        "blue", "default", "green", "red", "purple", "orange", "dark".
    Example option for changing the border color: ("color", "default")
    Width can be set using percent or pixels. Eg: "36.0%", "450px".
"""

self.get_jqc_form_inputs(message, buttons, options=None)
"""
Pop up a jquery-confirm box and return the input/button texts as tuple.
If running in headless mode, returns the ("", buttons[-1][0]) tuple.
@Params
message: The message to display in the jquery-confirm dialog.
buttons: A list of tuples for text and color.
    Example: [("Yes!", "green"), ("No!", "red")]
    Available colors: blue, green, red, orange, purple, default, dark.
    A simple text string also works: "My Button". (Uses default color.)
options: A list of tuples for options to set.
    Example: [("theme", "bootstrap"), ("width", "450px")]
    Available theme options: bootstrap, modern, material, supervan,
                             light, dark, and seamless.
    Available colors: (For the BORDER color, NOT the button color.)
        "blue", "default", "green", "red", "purple", "orange", "dark".
    Example option for changing the border color: ("color", "default")
    Width can be set using percent or pixels. Eg: "36.0%", "450px".
"""

self.set_jqc_theme(theme, color=None, width=None)
""" Sets the default jquery-confirm theme and width (optional).
Available themes: "bootstrap", "modern", "material", "supervan",
                  "light", "dark", and "seamless".
Available colors: (This sets the BORDER color, NOT the button color.)
    "blue", "default", "green", "red", "purple", "orange", "dark".
Width can be set using percent or pixels. Eg: "36.0%", "450px".
"""

self.reset_jqc_theme()
""" Resets the jqc theme settings to factory defaults. """

self.activate_jquery_confirm()  # Automatic for jqc methods
""" See https://craftpip.github.io/jquery-confirm/ for usage. """
```

--------

<h4>✅ 🛂 Automated/Manual Hybrid Mode (MasterQA)</h4>
<p><b><a href="https://seleniumbase.io/seleniumbase/masterqa/ReadMe/">MasterQA</a></b> uses <b>SeleniumBase Dialog Boxes</b> to speed up manual testing by having automation perform all the browser actions while the manual tester handles validation. See <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/master_qa">the MasterQA GitHub page</a> for examples.</p>
