<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) How to handle iframes

🖼️ <b>iframes</b> follow the same principle as new windows: You must first switch to the iframe if you want to perform actions in there:

```python
self.switch_to_frame("iframe")
# ... Now perform actions inside the iframe
self.switch_to_parent_frame()  # Exit the current iframe
```

To exit from multiple iframes, use ``self.switch_to_default_content()``. (If inside a single iframe, this has the same effect as ``self.switch_to_parent_frame()``.)

```python
self.switch_to_frame('iframe[name="frame1"]')
self.switch_to_frame('iframe[name="frame2"]')
# ... Now perform actions inside the inner iframe
self.switch_to_default_content()  # Back to the main page
```

🖼️ You can also use a context manager to act inside iframes:

```python
with self.frame_switch("iframe"):
    # ... Now perform actions while inside the code block
# You have left the iframe
```

This also works with nested iframes:

```python
with self.frame_switch('iframe[name="frame1"]'):
    with self.frame_switch('iframe[name="frame2"]'):
        # ... Now perform actions while inside the code block
    # You are now back inside the first iframe
# You have left all the iframes
```

🖼️ In special cases, you may want to set the page to the content of an iframe:

```python
self.set_content_to_frame("iframe")
```

To back out of one call of that, use:

```python
self.set_content_to_parent()
```

To back out of all nested calls of that, use:

```python
self.set_content_to_default()
```

🖼️ See [examples/iframe_tests.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/iframe_tests.py) for tests that use all available iframe commands.

--------

<p align="center"><div align="center"><a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20seleniumbase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a> <a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase.io Docs" /></a></div></p>
