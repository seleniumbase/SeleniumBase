<h2>Summary of existing Case Plans</h2>

|   |    |   |
| - | -: | - |
| 🔵 | 14 | Case Plans with customized tables |
| ⭕ | 0 | Case Plans using boilerplate code |
| 🚧 | 0 | Case Plans that are missing tables |

--------

<h3>🔎 (Click rows to expand) 🔍</h3>

<details>
<summary> 🔵 <code><b>basic_test.py::MyTestClass::test_basics</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Log in to https://www.saucedemo.com with ``standard_user``. | Login was successful. |
| 2 | Click on the ``Backpack`` ``ADD TO CART`` button. | The button text changed to ``REMOVE``. |
| 3 | Click on the cart icon. | The ``Backpack`` is seen in the cart. |
| 4 | Remove the ``Backpack`` from the cart. | The ``Backpack`` is no longer in the cart. |
| 5 | Log out from the website. | Logout was successful. |

</details>

<details>
<summary> 🔵 <code><b>my_first_test.py::MyTestClass::test_swag_labs</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Log in to https://www.saucedemo.com with ``standard_user``. | Login was successful. |
| 2 | Click on the ``Backpack`` ``ADD TO CART`` button. | The button text changed to ``REMOVE``. |
| 3 | Click on the cart icon. | The ``Backpack`` is seen in the cart. |
| 4 | Click on the ``CHECKOUT`` button. <br /> Enter user details and click ``CONTINUE``. | The ``Backpack`` is seen in the cart on the ``CHECKOUT: OVERVIEW`` page. |
| 5 | Click on the ``FINISH`` button. | There is a ``Thank you`` message. |
| 6 | Log out from the website. | Logout was successful. |

</details>

<details>
<summary> 🔵 <code><b>shadow_root_test.py::ShadowRootTest::test_shadow_root</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/other/shadow_dom. <br /> Click each tab and verify the text contained within the Shadow Root sections. | Tab 1 text: ``Content Panel 1`` <br /> Tab 2 text: ``Content Panel 2`` <br /> Tab 3 text: ``Content Panel 3`` |

</details>

<details>
<summary> 🔵 <code><b>test_assert_elements.py::ListAssertTests::test_assert_list_of_elements</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/demo_page. | |
| 2 | Use ``self.assert_elements_present("head", "style", "script")`` to verify that multiple elements are present in the HTML. | The assertion is successful. |
| 3 | Use ``self.assert_elements("h1", "h2", "h3")`` to verify that multiple elements are visible. | The assertion is successful. |
| 4 | Use ``self.assert_elements(["#myDropdown", "#myButton", "#svgRect"])`` to verify that multiple elements are visible. | The assertion is successful. |

</details>

<details>
<summary> 🔵 <code><b>test_calculator.py::CalculatorTests::test_6_times_7_plus_12_equals_54</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/apps/calculator. <br /> Perform the following calculation: ``6 × 7 + 12`` | The output is ``54`` after pressing ``=`` |

</details>

<details>
<summary> 🔵 <code><b>test_demo_site.py::DemoSiteTests::test_demo_site</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/demo_page |  |
| 2 | Assert the title of the current web page. <br /> Assert that a given element is visible on the page. <br /> Assert that a text substring appears in an element's text. | The assertions were successful. |
| 3 | Type text into various text fields and then verify. | The assertions were successful. |
| 4 | Verify that a hover dropdown link changes page text. | The assertion was successful. |
| 5 | Verify that a button click changes text on the page. | The assertion was successful. |
| 6 | Verify that an SVG element is located on the page. | The assertion was successful. |
| 7 | Verify that a slider control updates a progress bar. | The assertion was successful. |
| 8 | Verify that a "select" option updates a meter bar. | The assertion was successful. |
| 9 | Assert an element located inside an iFrame. | The assertion was successful. |
| 10 | Assert text located inside an iFrame. | The assertion was successful. |
| 11 | Verify that clicking a radio button selects it. | The assertion was successful. |
| 12 | Verify that clicking an empty checkbox makes it selected. | The assertion was successful. |
| 13 | Verify clicking on multiple elements with one call. | The assertions were successful. |
| 14 | Verify that clicking an iFrame checkbox selects it. | The assertions were successful. |
| 15 | Verify that Drag and Drop works. | The assertion was successful. |
| 16 | Assert link text. | The assertion was successful. |
| 17 | Verify clicking on link text. | The action was successful. |
| 18 | Assert exact text in an element. | The assertion was successful. |
| 19 | Highlight a page element. | The action was successful. |
| 20 | Verify that Demo Mode works. | The assertion was successful. |

</details>

<details>
<summary> 🔵 <code><b>test_login.py::SwagLabsLoginTests::test_swag_labs_login</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Log in to https://www.saucedemo.com with ``standard_user``. | Login was successful. |
| 2 | Log out from the website. | Logout was successful. |

</details>

<details>
<summary> 🔵 <code><b>test_mfa_login.py::TestMFALogin::test_mfa_login</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/realworld/login <br /> Enter credentials and Sign In. | Sign In was successful. |
| 2 | Click the ``This Page`` button. <br /> Save a screenshot to the logs. | |
| 3 | Click to Sign Out | Sign Out was successful. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/layout_test.py::VisualLayoutTests::test_applitools_layout_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://applitools.com/helloworld?diff1. <br /> Call ``check_window()`` with ``baseline=True``. <br /> Click the button that changes the text of an element. <br /> Call ``check_window()`` three times for ``level=1``, ``level=2``, and ``level=3``. | No issues are detected because a text change should not affect ``check_window()`` |
| 2 | Click the button that makes a hidden element visible. <br /> Call ``check_window()`` three times for ``level=1``, ``level=2``, and ``level=3``, but wrap the third call with ``self.assert_raises(Exception):``. | No exceptions are raised because the first two calls should pass and the third one was wrapped with ``self.assert_raises(Exception):``. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/python_home_test.py::VisualLayoutTests::test_python_home_layout_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://python.org/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Remove the ``Donate`` button using ``remove_element(SELECTOR)``. <br /> Call ``check_window()`` with ``level=0``. | The test detects that the ``Donate`` button was removed. The test does not fail because the check was set to ``level=0`` (print-only). <br /> A ``side_by_side_NAME.html`` file appears in the specific ``latest_logs/`` folder of the test. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/test_layout_fail.py::VisualLayout_FixtureTests::test_python_home_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://python.org/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Remove the ``Donate`` button using ``remove_element(SELECTOR)``. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the ``Donate`` button was removed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/test_layout_fail.py::VisualLayoutFailureTests::test_applitools_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://applitools.com/helloworld?diff1. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Click the button that makes a hidden element visible. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the element attribute has changed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/test_layout_fail.py::VisualLayoutFailureTests::test_xkcd_logo_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://xkcd.com/554/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Resize the logo using ``set_attribute()``. <br /> Call ``check_window()`` with ``level=3``. | The test fails because the logo has changed. <br /> A ``side_by_side.html`` file appears in the specific ``latest_logs/`` folder of the test. |

</details>

<details>
<summary> 🔵 <code><b>visual_testing/xkcd_visual_test.py::VisualLayoutTests::test_xkcd_layout_change</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://xkcd.com/554/. <br /> Call ``check_window()`` with ``baseline=True``. | |
| 2 | Resize the logo using ``set_attribute()``. <br /> Call ``check_window()`` with ``level=0``. | The test detects that the logo has changed. The test does not fail because the check was set to ``level=0`` (print-only). <br /> A ``side_by_side_NAME.html`` file appears in the specific ``latest_logs/`` folder of the test. |

</details>
