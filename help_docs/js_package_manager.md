[<img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> JS Package Manager</h2>

<div>SeleniumBase lets you load JavaScript packages from any CDN link into any website.</div>
<p><div>Here's an example of loading a website-tour library into the browser while visiting Google:</div></p>

<img src="https://cdn2.hubspot.net/hubfs/100006/google_tour_3.gif" title="SeleniumBase Tour of Google" /><br />

This example, ([google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py) from the SeleniumBase ``examples/tour_examples/`` folder), can be run with ``pytest`` after you've cloned and installed [SeleniumBase from GitHub](https://github.com/seleniumbase/SeleniumBase):

```bash
pytest google_tour.py
```

<div>Since a CDN is used for holding packages, you no longer need to use other package managers such as NPM, Bower, or Yarn.</div>
<p><div>Here's the Python code for loading JS packages into the web browser with SeleniumBase:</div></p>

```python
self.add_js_link(js_link)
```

<div>This example loads the <a href="https://introjs.com/">IntroJS</a> JavaScript library:</div>

```python
self.add_js_link("https://cdnjs.cloudflare.com/ajax/libs/intro.js/2.9.3/intro.min.js")
```

<div>You can load any JS package this way as long as you know the URL.</div>

If you're wondering how SeleniumBase does this, here's the full Python code, which uses WebDriver's ``execute_script()`` method for making JS calls after escaping quotes:

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

<p>Now that you've loaded JavaScript into the browser, you may also want to load some CSS to go along with it:</p>

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

<div>Website tours are just one of the many ways of using the SeleniumBase JS Package Manager.</div>
<p><div>The following example shows the <a href="https://github.com/craftpip/jquery-confirm">JqueryConfirm</a> package loaded into a website for creating fancy dialog boxes:</div></p>

<img src="https://cdn2.hubspot.net/hubfs/100006/images/masterqa6.gif" alt="MasterQA by SeleniumBase" title="MasterQA by SeleniumBase" /><br />

<p><div>(Example from <a href="https://seleniumbase.io/examples/master_qa/ReadMe/">SeleniumBase's MasterQA ReadMe</a>)</div></p>

<div>Since packages are loaded directly from a CDN, such as <a href="https://cdnjs.com/">CloudFlare's cdnjs</a>, there's no need to use NPM, Bower, Yarn, or other package managers to get the packages that you need into the websites that you want.</div>

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>

And if you're just interested in creating website tours with SeleniumBase, here's the link to the <a href="https://seleniumbase.io/examples/tour_examples/ReadMe/">Website Tours ReadMe</a>.
