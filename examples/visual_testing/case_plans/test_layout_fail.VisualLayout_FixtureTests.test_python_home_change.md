``test_layout_fail.py::VisualLayout_FixtureTests::test_python_home_change``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://python.org/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Remove the ``Donate`` button using ``remove_element(SELECTOR)``. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the ``Donate`` button was removed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |
