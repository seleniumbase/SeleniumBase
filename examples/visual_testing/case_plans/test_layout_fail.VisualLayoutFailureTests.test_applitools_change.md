``test_layout_fail.py::VisualLayoutFailureTests::test_applitools_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://applitools.com/helloworld?diff1. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Click the button that makes a hidden element visible. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the element attribute has changed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |
