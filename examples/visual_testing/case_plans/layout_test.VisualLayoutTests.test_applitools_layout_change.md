``layout_test.py::VisualLayoutTests::test_applitools_layout_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://applitools.com/helloworld?diff1. <br /> Call ``check_window()`` with ``baseline=True``. <br /> Click the button that changes the text of an element. <br /> Call ``check_window()`` three times for ``level=1``, ``level=2``, and ``level=3``. | No issues are detected because a text change should not affect ``check_window()`` |
| 2 | Click the button that makes a hidden element visible. <br /> Call ``check_window()`` three times for ``level=1``, ``level=2``, and ``level=3``, but wrap the third call with ``self.assert_raises(Exception):``. | No exceptions are raised because the first two calls should pass and the third one was wrapped with ``self.assert_raises(Exception):``. |
