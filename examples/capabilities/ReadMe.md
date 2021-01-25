### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Using Desired Capabilities

You can specify browser desired capabilities for webdriver when running SeleniumBase tests on a remote SeleniumGrid server such as [BrowserStack](https://www.browserstack.com/automate/capabilities), [Sauce Labs](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/), or [TestingBot](https://testingbot.com/support/other/test-options).

Sample run commands may look like this when run from the [SeleniumBase/examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder: (The browser is now specified in the capabilities file.)

```bash
pytest my_first_test.py --browser=remote --server=USERNAME:KEY@hub.browserstack.com --port=80 --cap_file=capabilities/sample_cap_file_BS.py
```

```bash
pytest my_first_test.py --browser=remote --server=USERNAME:KEY@ondemand.saucelabs.com --port=80 --cap_file=capabilities/sample_cap_file_SL.py
```

(Parameters: ``--browser=remote``, ``--server=SERVER``, ``--port=PORT``, and ``--cap_file=CAP_FILE.py``)

Here's an example desired capabilities file for BrowserStack:
```python
desired_cap = {
    'os': 'OS X',
    'os_version': 'High Sierra',
    'browser': 'Chrome',
    'browser_version': '77.0',
    'browserstack.local': 'false',
    'browserstack.selenium_version': '3.141.59'
}
```

Here's an example desired capabilities file for Sauce Labs:
```python
capabilities = {
    'browserName': 'firefox',
    'browserVersion': '70.0',
    'platformName': 'macOS 10.13',
    'sauce:options': {
    }
}
```

(You'll notice that the browser is now being specified in the capabilities file, rather than with ``--browser=BROWSER``)

<b>You can generate specific desired capabilities using:</b>
<ul>
    <li><a href="https://www.browserstack.com/automate/capabilities">BrowserStack desired capabilities</a></li>
    <li><a href="https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/">Sauce Labs desired capabilities</a></li>
    <li><a href="https://testingbot.com/support/other/test-options">TestingBot desired capabilities</a></li>
</ul>

<b>Parsing desired capabilities:</b>
SeleniumBase has a desired capabilities parser that can capture all lines from the specified file in the following formats:
``'KEY': 'VALUE'``
``'KEY': True``
``'KEY': False``
``caps['KEY'] = "VALUE"``
``caps['KEY'] = True``
``caps['KEY'] = False``
(Each pair must be on a separate line. You can interchange single and double quotes.)

You can also swap ``--browser=remote`` with an actual browser, eg ``--browser=chrome``, which will combine the default SeleniumBase desired capabilities with those that were specified in the capabilities file when using ``--cap_file=FILE.py``. Capabilities will override other parameters, so if you set the browser to one thing and the capabilities browser to another, SeleniumBase will use the capabilities browser as the browser.

You'll need default SeleniumBase capabilities for:
* Using a proxy server (not the same as a Selenium Grid server)
* Downloading files to a desired folder
* Disabling some warnings on Chrome
* Overriding a website's Content Security Policy on Chrome
* Other possible reasons

You can also set browser desired capabilities from a command line string:
Example:
```bash
pytest test_swag_labs.py --cap-string='{"browserName":"chrome","name":"test1"}' --server="127.0.0.1" --browser=remote
```
(Enclose cap-string in single quotes. Enclose parameter keys in double quotes.)

If you pass ``"*"`` into the ``"name"`` field of ``--cap-string``, the name will become the test identifier. Example:
```bash
pytest test_swag_labs.py --cap-string='{"browserName":"chrome","name":"*"}' --server="127.0.0.1" --browser=chrome
```
Example name: ``"my_first_test.MyTestClass.test_basics"``

### Using a local Selenium Grid

If using a local Selenium Grid with SeleniumBase, start up the Grid Hub and nodes first:
```bash
seleniumbase grid-hub start
seleniumbase grid-node start
```
(The Selenium Server JAR file will be automatically downloaded for first-time Grid users. You'll also need Java installed to start up the Grid.)
