### Using Desired Capabilities

You can specify browser desired capabilities for webdriver when running SeleniumBase tests on a remote SeleniumGrid server such as [BrowserStack](https://www.browserstack.com/automate/capabilities), [Sauce Labs](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/), or [TestingBot](https://testingbot.com/support/other/test-options).

Sample run commands may look like this when run from the [SeleniumBase/examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder: (The browser is now specified in the capabilities file.)

```bash
pytest my_first_test.py --browser=remote --server=USERNAME:KEY@hub.browserstack.com --port=80 --cap_file=capabilities/sample_cap_file_BS.py
```

```bash
pytest my_first_test.py --browser=remote --server=USERNAME:KEY@ondemand.saucelabs.com --port=80 --cap_file=capabilities/sample_cap_file_SL.py
```

(Parameters: ``--browser=remote``, ``--server=SERVER``, ``--port=PORT``, and ``--cap_file=CAP_FILE.py``)

Here's an example desired capabilities file:
```python
desired_cap = {
    'os': 'OS X',
    'os_version': 'Sierra',
    'browser': 'Chrome',
    'browser_version': '70.0',
    'browserstack.local': 'false',
    'browserstack.selenium_version': '3.14.0',
    'browserstack.chrome.driver': '2.43'
}
```

A desired capabilities file can also look like this:
```python
caps = {}
caps['browserName'] = "chrome"
caps['platform'] = "macOS 10.12"
caps['version'] = "70.0"
```

(You'll notice that the browser is now being specified in the capabilities file, rather than with ``--browser=BROWSER``)

You can generate desired capabilities for [BrowserStack](https://www.browserstack.com/automate/capabilities), [Sauce Labs](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/), and [TestingBot](https://testingbot.com/support/other/test-options) by following those links to their respective websites.

A regex parser was built into SeleniumBase to capture all lines from the specified desired capabilities file in the following formats:
``'KEY': 'VALUE'``
``'KEY': True``
``'KEY': False``
``caps['KEY'] = "VALUE"``
``caps['KEY'] = True``
``caps['KEY'] = False``
(Each pair must be on a separate line. You can interchange single and double quotes.)

You can also swap ``--browser=remote`` with an actual browser, eg ``--browser=chrome``, which will combine the default SeleniumBase desired capabilities with those that were specified in the capabilities file when using ``--cap_file=FILE.py``. Capabilities will override other parameters, so if you set the browser to one thing and the capabilities browser to another, SeleniumBase will use the capabilities browser as the browser. You'll need default SeleniumBase desired capabilities when using a proxy server (not the same as a Selenium Grid server), when downloading files to a desired folder, for disabling some warnings on Chrome, for overriding a website's Content Security Policy on Firefox, and for other reasons.
