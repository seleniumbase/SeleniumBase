<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) JS Package Manager and Code Generators

<h3>🕹️ SeleniumBase lets you load JavaScript packages from any CDN link into any website via Python.</h3>

<b>🎨 The following SeleniumBase solutions utilize this feature:</b>

🎦 (<a href="https://seleniumbase.io/help_docs/demo_mode/">Demo Mode</a>)

🚎 (<a href="https://seleniumbase.io/examples/tour_examples/ReadMe/">Website Tours</a>)

🎞️ (<a href="https://seleniumbase.io/examples/presenter/ReadMe/">Presentation Maker</a>)

📊 (<a href="https://seleniumbase.io/examples/chart_maker/ReadMe/">Chart Maker</a> / <a href="https://seleniumbase.io/examples/example_logs/ReadMe/">Dashboard</a>)

🛂 (<a href="https://seleniumbase.io/examples/dialog_boxes/ReadMe/">Dialog Boxes</a> / <a href="https://seleniumbase.io/examples/master_qa/ReadMe/">MasterQA</a>)

--------

<p><div>🗺️ Here's an example of loading a website-tour library into the browser for a Google Maps tour:</div></p>

<img src="https://seleniumbase.github.io/cdn/gif/introjs_tour.gif" title="SeleniumBase Tour of Google" /><br />

<p>🗺️ This example is from <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/maps_introjs_tour.py">maps_introjs_tour.py</a>. (The <code>--interval=1</code> makes the tour go automatically to the next step after 1 second.)</p>

```bash
cd examples/tour_examples
pytest maps_introjs_tour.py --interval=1
```

<p>🕹️ SeleniumBase includes powerful JS code generators for converting Python into JavaScript for using the supported JS packages. A few lines of Python in your tests might generate hundreds of lines of JavaScript.</p>

<p>🗺️ Here is some tour code in Python from <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/maps_introjs_tour.py">maps_introjs_tour.py</a> that expands into a lot of JavaScript.</p>

```python
self.open("https://www.google.com/maps/@42.3591234,-71.0915634,15z")
self.create_tour(theme="introjs")
self.add_tour_step("Welcome to Google Maps!", title="SeleniumBase Tours")
self.add_tour_step("Enter Location", "#searchboxinput", title="Search Box")
self.add_tour_step("See it", "#searchbox-searchbutton", alignment="bottom")
self.add_tour_step("Thanks for using Tours!", title="End of Guided Tour")
self.export_tour(filename="maps_introjs_tour.js")
self.play_tour()
```

<p><div>🕹️ For existing features, SeleniumBase already takes care of loading all the necessary JS and CSS files into the web browser. To load other packages, here are a few useful methods that you should know about:</div></p>

```python
self.add_js_link(js_link)
```

<p><div>🕹️ This example loads the <a href="https://introjs.com/">IntroJS</a> JavaScript library:</div></p>

```python
self.add_js_link("https://cdnjs.cloudflare.com/ajax/libs/intro.js/2.9.3/intro.min.js")
```

<div>🕹️ You can load any JS package this way as long as you know the URL.</div>

<p>🕹️ If you're wondering how SeleniumBase does this, here's the full Python code from <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/js_utils.py">js_utils.py</a>, which uses WebDriver's <code>execute_script()</code> method for making JS calls after escaping quotes with backslashes as needed:</p>

```python
def add_js_link(driver, js_link):
    script_to_add_js = (
        """function injectJS(link) {
              var body = document.getElementsByTagName("body")[0];
              var script = document.createElement("script");
              script.src = link;
              script.defer;
              script.type="text/javascript";
              script.crossorigin = "anonymous";
              script.onload = function() { null };
              body.appendChild(script);
           }
           injectJS("%s");""")
    js_link = escape_quotes_if_needed(js_link)
    driver.execute_script(script_to_add_js % js_link)
```

<p>🕹️ Now that you've loaded JavaScript into the browser, you may also want to load some CSS to go along with it:</p>

```python
self.add_css_link(css_link)
```

<p>🕹️ Here's code that loads the <a href="https://introjs.com/">IntroJS</a> CSS:</p>

```python
self.add_css_link("https://cdnjs.cloudflare.com/ajax/libs/intro.js/2.9.3/introjs.css")
```

<p>🕹️ And here's the Python WebDriver code that makes this possible:</p>

```python
def add_css_link(driver, css_link):
    script_to_add_css = (
        """function injectCSS(css) {
              var head = document.getElementsByTagName("head")[0];
              var link = document.createElement("link");
              link.rel = "stylesheet";
              link.type = "text/css";
              link.href = css;
              link.crossorigin = "anonymous";
              head.appendChild(link);
           }
           injectCSS("%s");""")
    css_link = escape_quotes_if_needed(css_link)
    driver.execute_script(script_to_add_css % css_link)
```

<div>🕹️ Website tours are just one of the many uses of the JS Package Manager.</div>
<p><div>🛂 The following example shows the <a href="https://github.com/craftpip/jquery-confirm">JqueryConfirm</a> package loaded into a website for creating fancy dialog boxes:</div></p>

<img src="https://seleniumbase.github.io/cdn/img/emoji_sports_dialog.png" alt="SeleniumBase" width="480" />

<h4>↕️ (<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/dialog_boxes/dialog_box_tour.py">Example: dialog_box_tour.py</a>) ↕️</h4>

<img src="https://seleniumbase.github.io/cdn/gif/sports_dialog.gif" alt="SeleniumBase" width="480" />

<h4>Here's how to run that example:</h4>

```bash
cd examples/dialog_boxes
pytest test_dialog_boxes.py
```

<p><div>(Example from the <a href="https://seleniumbase.io/examples/dialog_boxes/ReadMe/">Dialog Boxes ReadMe</a>)</div></p>

<div>🕹️ Since packages are loaded directly from a CDN link, you won't need other package managers like NPM, Bower, or Yarn to get the packages that you need into the websites that you want.</div>

--------

[<img src="https://seleniumbase.github.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="220">](https://github.com/seleniumbase/SeleniumBase/)

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
