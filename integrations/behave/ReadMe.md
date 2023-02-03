<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 🐝 Behave test runner for SeleniumBase 🐝</h2>

🐝 (Utilizes the [Behave BDD Python library](https://github.com/behave/behave). For more info, see the [Behave tutorial](https://behave.readthedocs.io/en/stable/tutorial.html) and read about [Behave's Gherkin model](https://behave.readthedocs.io/en/stable/gherkin.html).)

🐝 Behave examples with SeleniumBase: [SeleniumBase/examples/behave_bdd](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd)

```bash
> cd examples/behave_bdd/
> behave features/realworld.feature -T -D dashboard -k

Dashboard: /Users/michael/github/SeleniumBase/examples/behave_bdd/dashboard.html
********************************************************************************
Feature: SeleniumBase scenarios for the RealWorld App # features/realworld.feature:1

  Scenario: Verify RealWorld App (log in / sign out)  # features/realworld.feature:3
    Given Open the RealWorld Login Page               # steps/real_world.py:4
    When Login to the RealWorld App                   # steps/real_world.py:11
    Then Assert exact text "Welcome!" in "h1"         # steps/real_world.py:89
    When Highlight element "img#image1"               # steps/real_world.py:19
    And Click element 'a:contains("This Page")'       # steps/real_world.py:29
    Then Save a screenshot to the logs                # steps/real_world.py:49
    When Click link "Sign out"                        # steps/real_world.py:39
    Then Assert element 'a:contains("Sign in")'       # steps/real_world.py:55
    And Assert text "You have been signed out!"       # steps/real_world.py:79
   ✅ Scenario Passed!

- Dashboard: /Users/michael/github/SeleniumBase/examples/behave_bdd/dashboard.html
--- LogPath: /Users/michael/github/SeleniumBase/examples/behave_bdd/latest_logs/
==================================================================================
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
12 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m4.682s
```

🐝 Another example, which uses higher-level Behave steps to simplify the ``.feature`` file:

```bash
> cd examples/behave_bdd/
> behave features/calculator.feature:61 -T -D dashboard -k

Dashboard: /Users/michael/github/SeleniumBase/examples/behave_bdd/dashboard.html
********************************************************************************
Feature: SeleniumBase scenarios for the Calculator App # features/calculator.feature:1

  Background:   # features/calculator.feature:3

  Scenario: 7.0 × (3 + 3) = 42        # features/calculator.feature:49
    Given Open the Calculator App     # features/steps/calculator.py:4
    When Press C                      # features/steps/calculator.py:9
    And Press 7                       # features/steps/calculator.py:79
    And Press .                       # features/steps/calculator.py:104
    And Press 0                       # features/steps/calculator.py:94
    And Press ×                       # features/steps/calculator.py:29
    And Press (                       # features/steps/calculator.py:14
    And Press 3                       # features/steps/calculator.py:59
    And Press +                       # features/steps/calculator.py:39
    And Press 3                       # features/steps/calculator.py:59
    And Press )                       # features/steps/calculator.py:19
    Then Verify output is "7.0×(3+3)" # features/steps/calculator.py:135
    When Press =                      # features/steps/calculator.py:44
    Then Verify output is "42"        # features/steps/calculator.py:135
   ✅ Scenario Passed!

- Dashboard: /Users/michael/github/SeleniumBase/examples/behave_bdd/dashboard.html
--- LogPath: /Users/michael/github/SeleniumBase/examples/behave_bdd/latest_logs/
==================================================================================
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 8 skipped
14 steps passed, 0 failed, 60 skipped, 0 undefined
Took 0m1.672s
```

🐝⚪ With the Dashboard enabled, you'll get one of these:

<img src="https://seleniumbase.github.io/cdn/img/sb_behave_dashboard.png" title="SeleniumBase" width="600">

### 🐝 Behave-Gherkin files:

🐝 The ``*.feature`` files can use any step seen from:

```bash
behave --steps-catalog
```

🐝 SeleniumBase includes several pre-made Behave steps, which you can use by creating a Python file with the following line in your ``features/steps/`` directory:

```python
from seleniumbase.behave import steps  # noqa
```

🐝 Inside your ``features/environment.py`` file, you should have the following:

```python
from seleniumbase import BaseCase
from seleniumbase.behave import behave_sb
behave_sb.set_base_class(BaseCase)  # Accepts a BaseCase subclass
from seleniumbase.behave.behave_sb import before_all  # noqa
from seleniumbase.behave.behave_sb import before_feature  # noqa
from seleniumbase.behave.behave_sb import before_scenario  # noqa
from seleniumbase.behave.behave_sb import before_step  # noqa
from seleniumbase.behave.behave_sb import after_step  # noqa
from seleniumbase.behave.behave_sb import after_scenario  # noqa
from seleniumbase.behave.behave_sb import after_feature  # noqa
from seleniumbase.behave.behave_sb import after_all  # noqa
```

🐝 If you've already created a subclass of ``BaseCase`` with custom methods, you can swap ``BaseCase`` in with your own subclass, which will allow you to easily use your own custom methods in your Behave step definitions.

🐝 Here's an example Python file in the ``features/steps/`` folder:

```python
from behave import step


@step("Open the Swag Labs Login Page")
def go_to_swag_labs(context):
    sb = context.sb
    sb.open("https://www.saucedemo.com")
    sb.clear_local_storage()


@step("Login to Swag Labs with {user}")
def login_to_swag_labs(context, user):
    sb = context.sb
    sb.type("#user-name", user)
    sb.type("#password", "secret_sauce\n")


@step("Verify that the current user is logged in")
def verify_logged_in(context):
    sb = context.sb
    sb.assert_element("#header_container")
    sb.assert_element("#react-burger-menu-btn")
    sb.assert_element("#shopping_cart_container")


@step('Add "{item}" to cart')
def add_item_to_cart(context, item):
    sb = context.sb
    sb.click('div.inventory_item:contains("%s") button[name*="add"]' % item)
```

🐝 A ``*.feature`` file could look like this:

```gherkin
Feature: SeleniumBase scenarios for the Swag Labs App

  Background:
    Given Open the Swag Labs Login Page

  Scenario: User can order a backpack from the store
    When Login to Swag Labs with standard_user
    Then Verify that the current user is logged in
    And Save price of "Backpack" to <item_price>
    When Add "Backpack" to Cart
    Then Verify shopping cart badge shows 1 item(s)
    When Click on shopping cart icon
    And Click Checkout
    And Enter checkout info: First, Last, 12345
    And Click Continue
    Then Verify 1 "Backpack"(s) in cart
    And Verify cost of "Backpack" is <item_price>
    And Verify item total is $29.99
    And Verify tax amount is $2.40
    And Verify total cost is $32.39
    When Click Finish
    Then Verify order complete
    When Logout from Swag Labs
    Then Verify on Login page
```

🐝 Here's another example of a ``*.feature`` file:

```gherkin
Feature: SeleniumBase scenarios for the RealWorld App

  Scenario: Verify RealWorld App (log in / sign out)
    Given Open "seleniumbase.io/realworld/login"
    And Clear Session Storage
    When Type "demo_user" into "#username"
    And Type "secret_pass" into "#password"
    And Do MFA "GAXG2MTEOR3DMMDG" into "#totpcode"
    Then Assert text "Welcome!" in "h1"
    And Highlight element "img#image1"
    And Click 'a:contains("This Page")'
    And Save screenshot to logs
    When Click link "Sign out"
    Then Assert element 'a:contains("Sign in")'
    And Assert text "You have been signed out!"
```

🐝 If there's a test failure, that's easy to spot:

```bash
Feature: SeleniumBase scenarios for the Fail Page # features/fail_page.feature:1

  Scenario: Fail test on purpose to see what happens  # features/fail_page.feature:3
    When Open the Fail Page                           # features/steps/fail_page.py:4
    Then Fail test on purpose                         # features/steps/fail_page.py:9
      Assertion Failed: This test fails on purpose!
      Captured stdout:
      >>> STEP FAILED:  (#2) Fail test on purpose
      Class / Feature:  SeleniumBase scenarios for the Fail Page
      Test / Scenario:  Fail test on purpose to see what happens

   ❌ Scenario Failed!
```

🐝🎖️ For convenience, the [SeleniumBase Behave GUI](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/behave_gui.md) lets you run ``behave`` scripts from a Desktop app.

🐝🎖️ To launch it, call ``sbase behave-gui`` or ``sbase gui-behave``:

```bash
sbase behave-gui
* Starting the SeleniumBase Behave Commander GUI App...
```

<img src="https://seleniumbase.github.io/cdn/img/sbase_behave_gui_wide_5.png" title="SeleniumBase" width="600">

🐝🎖️ You can customize the tests that show up there:

```bash
sbase behave-gui  # all tests
sbase behave-gui -i=calculator  # tests with "calculator" in the name
sbase behave-gui features/  # tests located in the "features/" folder
sbase behave-gui features/calculator.feature  # tests in that feature
```

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
