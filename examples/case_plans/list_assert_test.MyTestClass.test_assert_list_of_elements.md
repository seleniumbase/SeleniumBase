``list_assert_test.py::MyTestClass::test_assert_list_of_elements``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/demo_page. | |
| 2 | Use ``self.assert_elements_present("head", "style", "script")`` to verify that multiple elements are present in the HTML. | The assertion is successful. |
| 3 | Use ``self.assert_elements("h1", "h2", "h3")`` to verify that multiple elements are visible. | The assertion is successful. |
| 4 | Use ``self.assert_elements(["#myDropdown", "#myButton", "#svgRect"])`` to verify that multiple elements are visible. | The assertion is successful. |
