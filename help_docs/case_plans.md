<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) SeleniumBase Case Plans 🗂️

<img src="https://seleniumbase.github.io/cdn/img/cp/sb_case_plans.png" title="SeleniumBase Case Plans Summary" width="625">

🗂️ <b>SeleniumBase Case Plans</b> is Test Case Management Software that uses Markdown tables for displaying test plans directly in GitHub (and other source code management systems that support Markdown format).

🗂️ The ``case_summary.md`` file is generated from individual Case Plans that exist in the ``case_plans/`` folders of your repository. (See the example below to learn how the Case Summary file may look.)

--------

> **Example of a ``case_summary.md`` file:**

<h2>Summary of existing Case Plans</h2>

|   |    |   |
| - | -: | - |
| 🔵 | 8 | Case Plans with customized tables |
| ⭕ | 2 | Case Plans using boilerplate code |
| 🚧 | 1 | Case Plan that is missing a table |

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
<summary> 🔵 <code><b>list_assert_test.py::MyTestClass::test_assert_list_of_elements</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/demo_page. | |
| 2 | Use ``self.assert_elements_present("head", "style", "script")`` to verify that multiple elements are present in the HTML. | The assertion is successful. |
| 3 | Use ``self.assert_elements("h1", "h2", "h3")`` to verify that multiple elements are visible. | The assertion is successful. |
| 4 | Use ``self.assert_elements(["#myDropdown", "#myButton", "#svgRect"])`` to verify that multiple elements are visible. | The assertion is successful. |

</details>

<details>
<summary> ⭕ <code><b>locale_code_test.py::LocaleCodeTests::test_locale_code</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Perform Action 1 | Verify Action 1 |
| 2 | Perform Action 2 | Verify Action 2 |

</details>

<details>
<summary> 🔵 <code><b>my_first_test.py::MyTestClass::test_swag_labs</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Log in to https://www.saucedemo.com with ``standard_user``. | Login was successful. |
| 2 | Click on the ``Backpack`` ``ADD TO CART`` button. | The button text changed to ``REMOVE``. |
| 3 | Click on the cart icon. | The ``Backpack`` is seen in the cart. |
| 4 | Click on the ``CHECKOUT`` button. <br /> Enter user details and click ``CONTINUE``. | The ``Backpack`` is seen in the cart on the ``CHECKOUT: OVERVIEW`` page. |
| 5 | Click on the ``FINISH`` button. | There is a ``Thank You`` message and a ``Pony Express`` delivery logo. |
| 6 | Log out from the website. | Logout was successful. |

</details>

<details>
<summary> ⭕ <code><b>proxy_test.py::ProxyTests::test_proxy</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Perform Action 1 | Verify Action 1 |
| 2 | Perform Action 2 | Verify Action 2 |

</details>

<details>
<summary> 🔵 <code><b>shadow_root_test.py::ShadowRootTest::test_shadow_root</b></code></summary>

| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Open https://seleniumbase.io/other/shadow_dom. <br /> Click each tab and verify the text contained within the Shadow Root sections. | Tab 1 text: ``Content Panel 1`` <br /> Tab 2 text: ``Content Panel 2`` <br /> Tab 3 text: ``Content Panel 3`` |

</details>

🚧 <code><b>test_agent.py::UserAgentTests::test_user_agent</b></code>

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

--------

🗂️ Before you can generate a ``case_summary.md`` file that includes your existing Case Plans, first you'll need to select which existing tests you want to create boilerplate Case Plans from. For that, you can use the SeleniumBase Case Plans GUI:

```bash
sbase caseplans
```

<img src="https://seleniumbase.github.io/cdn/img/cp/case_plan_boilerplate_gen.png" title="SeleniumBase Case Plans GUI" width="525">

🗂️ Once you are running the Case Plans GUI, select the existing tests that need Case Plans, and then click: ``Generate boilerplate Case Plans for selected tests missing them``. For each selected test that didn't already have a Case Plan file, one will be generated. Each new Case Plan file starts with default boilerplate code with a Markdown table. Eg:

```bash
``proxy_test.py::ProxyTests::test_proxy``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Perform Action 1 | Verify Action 1 |
| 2 | Perform Action 2 | Verify Action 2 |

```

🗂️ When rendered as a Markdown table, the result looks like this:

``proxy_test.py::ProxyTests::test_proxy``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Perform Action 1 | Verify Action 1 |
| 2 | Perform Action 2 | Verify Action 2 |

🗂️ Markdown tables are flexible, but must be constructed correctly to be displayed. For a Markdown table to render, it's important that you place pipes (``|``), dashes (``-``), and spaces in the correct locations. If you want a line break in a step, use ``<br />``. If you want an empty step, put a space between pipes, eg: ``| |``.

🗂️ Here's an example of a Case Plan for [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py):

``my_first_test.py::MyTestClass::test_swag_labs``
---
| # | Step Description | Expected Result |
| - | ---------------- | --------------- |
| 1 | Log in to https://www.saucedemo.com with ``standard_user``. | Login was successful. |
| 2 | Click on the ``Backpack`` ``ADD TO CART`` button. | The button text changed to ``REMOVE``. |
| 3 | Click on the cart icon. | The ``Backpack`` is seen in the cart. |
| 4 | Click on the ``CHECKOUT`` button. <br /> Enter user details and click ``CONTINUE``. | The ``Backpack`` is seen in the cart on the ``CHECKOUT: OVERVIEW`` page. |
| 5 | Click on the ``FINISH`` button. | There is a ``Thank you`` message. |
| 6 | Log out from the website. | Logout was successful. |

🗂️ After you've created some Case Plans, you can use the ``Generate Summary of existing Case Plans`` button in the Case Plans GUI to generate the Case Plans Summary file.

<img src="https://seleniumbase.github.io/cdn/img/cp/case_plan_summary_gen.png" title="SeleniumBase Case Plans GUI" width="550">

🗂️ The generated Case Plans summary file, ``case_summary.md``, gets created in the same location where the Case Plans GUI was launched. This is NOT the same location where individual Case Plan boilerplates are generated, which is in the ``case_plans/`` folders. The ``case_plans/`` folders are generated where individual tests live, which means that if you have your tests in multiple folders, then you could also have multiple ``case_plans/`` folders. A ``case_summary.md`` file may look like this when rendered:

<img src="https://seleniumbase.github.io/cdn/img/cp/case_plan_summary.png" title="SeleniumBase Case Plans Summary" width="550">

🗂️ When calling ``sbase caseplans``, you can provide additional arguments to limit the tests that appear in the list. The same discovery rules apply as when using ``pytest``. Eg:

```bash
sbase caseplans
sbase caseplans -k agent
sbase caseplans -m marker2
sbase caseplans test_suite.py
sbase caseplans offline_examples/
```

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20View%20Code-on%20GitHub%20🌎-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
