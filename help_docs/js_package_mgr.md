<p><h3 align="center"><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb23.png" alt="SeleniumBase" width="220" /></a></h3></p>

## JS Package Manager

<div>The SeleniumBase JS Package Manager lets you load any JavaScript library into any website from automation scripts.</div>
<p><div>Here's an example of website-tour libraries loaded into a browser session while visiting Google:</div></p>

<img src="https://cdn2.hubspot.net/hubfs/100006/google_tour_3.gif" title="SeleniumBase Tour of Google"><br />

This example from [google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py) can be run with <b>pytest</b> from the SeleniumBase ``examples/tour_examples`` folder with the following command after you've cloned and installed [SeleniumBase from GitHub](https://github.com/seleniumbase/SeleniumBase):

```bash
pytest google_tour.py
```

<div>Website tours are just one way of demonstrating the abilities of the SeleniumBase JS Package Manager.</div>
<div>Here's the SeleniumBase code for loading any JS package into any website from your web browser:</div>

```python
self.add_js_link(js_link)
```

Here's code that loads the <a href="https://introjs.com/">IntroJS</a> JavaScript library:

```python
self.add_js_link("https://cdnjs.cloudflare.com/ajax/libs/intro.js/2.9.3/intro.min.js")
```

<div>You can load any JS library into a web browser this way as long as you know the URL to it!</div>

If you're wondering how SeleniumBase does this, here's a sneak peak at the code, which uses WebDriver's ``execute_script()`` method to run JavaScript commands:

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

<p>Now that you've loaded the JavaScript into the browser, you may also want to load some CSS to go along with it:</p>

```python
self.add_css_link(css_link)
```

<p>Here's code that loads the <a href="https://introjs.com/">IntroJS</a> CSS:</p>

```python
self.add_css_link("https://cdnjs.cloudflare.com/ajax/libs/intro.js/2.9.3/introjs.css")
```

<p>And here's the Python WebDriver code that makes this possible:</p>

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

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>

And if you're just interested in creating website tours with SeleniumBase, here's the link to the <a href="https://seleniumbase.io/examples/tour_examples/ReadMe/">Website Tours ReadMe</a>.
