<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> The HTML Inspector</h2>

🔵 <b>HTML Inspector</b> provides useful info about a web page.

🔵 (<i>Based on: [github.com/philipwalton/html-inspector](https://github.com/philipwalton/html-inspector)</i>)

🔵 Example: [examples/test_inspect_html.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_inspect_html.py) (Chromium-only)

```python
from seleniumbase import BaseCase

class HtmlInspectorTests(BaseCase):
    def test_html_inspector(self):
        self.open("https://xkcd.com/1144/")
        self.inspect_html()
```

--------

```bash
pytest test_inspect_html.py 
============== test session starts ==============

* HTML Inspection Results: https://xkcd.com/1144/
X - https://xkcd.com/1144/ - Access to XMLHttpRequest at 'https://xkcd.com/usBanner' (redirected from 'https://c.xkcd.com/xkcd/news') from origin 'https://xkcd.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
X - https://xkcd.com/usBanner - Failed to load resource: net::ERR_FAILED
X - 'property' is not a valid attribute of the <meta> element.
X - Do not use <div> or <span> elements without any attributes.
X - The 'alt' attribute is required for <img> elements.
X - The 'border' attribute is no longer valid on the <img> element and should not be used.
X - 'srcset' is not a valid attribute of the <img> element.
X - The <center> element is obsolete and should not be used.
X - <script> elements should appear right before the closing </body> tag for optimal performance.
X - The id 'comicLinks' appears more than once in the document.
* (See the Console output for details!)
```
