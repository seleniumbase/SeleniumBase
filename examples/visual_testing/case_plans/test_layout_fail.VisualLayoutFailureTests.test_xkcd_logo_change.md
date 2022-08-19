``test_layout_fail.py::VisualLayoutFailureTests::test_xkcd_logo_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://xkcd.com/554/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Resize the logo using ``set_attribute()``. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the logo has changed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |
