<!-- SeleniumBase Docs -->

## ✅ Support for migrating from raw Selenium to SeleniumBase


### 🔵 Here are some examples that can help you understand how to migrate from raw Selenium to SeleniumBase

The five main examples in the [examples/migration/raw_selenium](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium) folder are:

* [flaky_messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/flaky_messy_raw.py)
* [long_messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/long_messy_raw.py)
* [messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/messy_raw.py)
* [refined_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/refined_raw.py)
* [simple_sbase.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/simple_sbase.py)

Each of these examples is structured as a test that can be run with ``pytest``. They all inherit ``unittest.TestCase`` either directly, or via ``seleniumbase.BaseCase``, which extends it. This provides automatically-called ``setUp()`` and ``tearDown()`` methods before and after each test.

> These examples show the evolution of tests from raw Selenium to SeleniumBase. By understanding common progressions of Selenium engineers, you can avoid making the same mistakes as they did, and learn to write good tests efficiently without the long learning curve.

* [flaky_messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/flaky_messy_raw.py)

This is common example of how newcomers to Selenium write tests (assuming they've already learned how to break out reusuable code into ``setUp()`` and ``tearDown()`` methods). It uses ``find_element()`` calls, which can lead to flaky tests because those calls fail if a page element is slow to load.

* [long_messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/long_messy_raw.py)

At the next stage of learning, newcomers to Selenium realize that their tests are flaky, so they start replacing existing ``find_element()`` calls with ``WebDriverWait`` and internal Selenium ``expected_conditions`` methods, such as ``visibility_of_element_located`` and ``element_to_be_clickable``. This can result in long/messy tests that are unmaintainable if not written carefully.

* [messy_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/messy_raw.py)

By this stage, newcomers to Selenium have evolved into legitimate test automation engineers. They have become better at writing reusable code, so they've broken down the long ``WebDriverWait`` and ``expected_conditions`` calls into shorter method calls, which are easier to read, but could still be improved on for better maintainability. Here, individual page actions are still written out as multiple lines of code, (or multiple method calls per line), which isn't efficient.

* [refined_raw.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/refined_raw.py)

By now, the test automation engineer has become an expert in breaking out code into reusable methods, and the test itself has been simplified down to a single page action per line. The code is easy to read and easy to maintain. The error output is also simplified. The journey of writing a complete test automation framework for Selenium has begun.

* [simple_sbase.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium/simple_sbase.py)

With a complete test automation framework built, most of the hard work is already done for you. By importing ``BaseCase`` into your test classes, your tests gain access to all SeleniumBase methods, which can simplify your code. SeleniumBase also provides a lot of additional functionality that isn't included with raw Selenium.


### 🔵 How is SeleniumBase different from raw Selenium?

<div>
<p>💡 SeleniumBase is a Python test framework for the <a href="https://www.w3.org/TR/webdriver2/#endpoints" target="_blank">Selenium/WebDriver</a> browser automation library. This framework incorporates test-runners such as <code>pytest</code>, <code>nosetests</code>, and <code>behave</code> to provide organized structure, test discovery, test execution, test state (<i>eg. passed, failed, or skipped</i>), and command-line options for changing default settings (<i>such as choosing the browser to use</i>). With raw Selenium, you would need to set up your own options-parser for configuring tests from the command-line.</p>

<p>💡 With raw Selenium, you have to manually download drivers (<i>eg. chromedriver</i>) before running tests. With SeleniumBase's driver manager, that's done automatically for you if the required driver isn't already on your PATH. There are also console scripts available for more control (eg. <code>sbase get chromedriver latest</code> to download the latest version of chromedriver to a local SeleniumBase directory).</p>

<p>💡 With raw Selenium, commands that use selectors need to specify the type of selector (eg. <code>"css selector", "button#myButton"</code>). With SeleniumBase, there's auto-detection between CSS Selectors and XPath, which means you don't need to specify the type of selector in your commands (<i>but optionally you could</i>).</p>

<p>💡 SeleniumBase methods often perform multiple actions in a single method call. For example, <code>self.type(selector,text)</code> does the following:<br />1. Waits for the element to be visible.<br />2. Waits for the element to be interactive.<br />3. Clears the text field.<br />4. Types in the new text.<br />5. Presses Enter/Submit if the text ends in "\n".<br />With raw Selenium, those actions require multiple method calls.</p>

<p>💡 SeleniumBase uses default timeout values when not set, which means that methods automatically wait for elements to appear (<i>up to the timeout limit</i>) before failing:<br />✅<code>self.click("button")</code><br />With raw Selenium, methods would fail instantly (<i>by default</i>) if an element needed more time to load:<br />❌<code>self.driver.find_element(by="css selector", value="button").click()</code><br />(Reliable code is better than unreliable code.)</p>

<p>💡 SeleniumBase lets you change the explicit timeout values of methods:<br />✅<code>self.click("button",timeout=10)</code><br />With raw Selenium, that requires more code:<br />❌<code>WebDriverWait(driver,10).until(EC.element_to_be_clickable("css selector", "button")).click()</code><br />(Simple code is better than complex code.)</p>

<p>💡 SeleniumBase gives you clean error output when a test fails. With raw Selenium, error messages can get very messy.</p>

<p>💡 SeleniumBase gives you the option to generate a dashboard and reports for tests. It also saves screenshots from failing tests to the <code>./latest_logs/</code> folder. Raw Selenium does not have these options out-of-the-box.</p>

<p>💡 SeleniumBase includes desktop GUI apps for running tests, such as <b>SeleniumBase Commander</b> for <code>pytest</code>, and <b>SeleniumBase Behave GUI.</b></p>

<p>💡 SeleniumBase has its own Recorder & Test Generator that can create tests from manual browser actions. SeleniumBase also has many other useful tools and console scripts for getting things done quickly. (<i>See the documentation for more details!</i>)</p>
</div>

--------

[<img src="https://seleniumbase.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase)
