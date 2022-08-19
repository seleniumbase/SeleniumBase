``python_home_test.py::VisualLayoutTests::test_python_home_layout_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://python.org/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Remove the ``Donate`` button using ``remove_element(SELECTOR)``. <br /> Call ``check_window()`` with ``level=0``. | The test detects that the ``Donate`` button was removed. The test does not fail because the check was set to ``level=0`` (print-only). <br /> A ``side_by_side_NAME.html`` file appears in the specific ``latest_logs/`` folder of the test. |
