## [<img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) The HTML Inspector 🔎

🔎 <b>HTML Inspector</b> provides useful info about a web page.

🔎 (<i>Based on: [github.com/philipwalton/html-inspector](https://github.com/philipwalton/html-inspector)</i>)

🔎 Example: [examples/test_inspect_html.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_inspect_html.py) (Chromium-only)

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
X - 'property' is not a valid attribute of the <meta> element.
X - Do not use <div> or <span> elements without any attributes.
X - 'srcset' is not a valid attribute of the <img> element.
X - The 'border' attribute is no longer valid on the <img> element and should not be used.
X - The <center> element is obsolete and should not be used.
X - <script> elements should appear right before the closing </body> tag for optimal performance.
X - The id 'comicLinks' appears more than once in the document.
* (See the Console output for details!)
```
