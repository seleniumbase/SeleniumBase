<!-- SeleniumBase Docs -->

<h3 align="left"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_b.png" alt="SeleniumBase" width="300" /></h3>

## Shadow DOM support / Shadow-root interaction

🔵 SeleniumBase lets you pierce through open Shadow DOM selectors (to interact with elements inside) by adding ``::shadow`` to CSS fragments that include a shadow-root element. For multi-layered shadow-roots, you must individually pierce through each shadow-root element that you want to get through.

🔵 Here are some examples of Shadow DOM selectors:

```python
css_1 = "downloads-manager::shadow #no-downloads"

css_2 = "downloads-manager::shadow #downloadsList downloads-item::shadow #file-link"

css_3 = "downloads-manager::shadow downloads-toolbar::shadow cr-toolbar::shadow cr-toolbar-search-field::shadow cr-icon-button"

css_4 = "downloads-manager::shadow downloads-toolbar::shadow cr-toolbar::shadow cr-toolbar-search-field::shadow #searchInput"

css_5 = "downloads-manager::shadow downloads-toolbar::shadow cr-toolbar::shadow cr-toolbar-search-field::shadow #clearSearch"
```

🔵 The shadow-root (``::shadow``) elements are transitional, and therefore cannot be the final part of your CSS selectors. Complete your CSS selectors by including an element that's inside a shadow-root.

🔵 NOTE: ``::shadow`` selectors only exist within SeleniumBase. (They are not part of standard CSS.)

🔵 Here are some examples of tests that interact with Shadow DOM elements:
* [examples/shadow_root_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/shadow_root_test.py)
* [examples/test_shadow_dom.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_shadow_dom.py)
* [examples/old_wordle_script.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/old_wordle_script.py)
