``xkcd_visual_test.py::VisualLayoutTests::test_xkcd_layout_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://xkcd.com/554/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Resize the logo using ``set_attribute()``. <br /> Call ``check_window()`` with ``level=0``. | The test detects that the logo has changed. The test does not fail because the check was set to ``level=0`` (print-only). <br /> A ``side_by_side_NAME.html`` file appears in the specific ``latest_logs/`` folder of the test. |
