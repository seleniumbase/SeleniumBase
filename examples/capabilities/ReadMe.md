### Using Desired Capabilities

You can specify browser desired capabilities for webdriver when running SeleniumBase tests on a remote SeleniumGrid server such as [BrowserStack](https://www.browserstack.com/automate/capabilities), [Sauce Labs](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/), or [TestingBot](https://testingbot.com/support/other/test-options).

A sample run command may look like this: (When run from the ``SeleniumBase/examples/`` folder):

```bash
pytest my_first_test.py --browser=remote --server=username:key@hub.browserstack.com --port=80 --cap_file=capabilities/sample_cap_file_BS.py
```

A regex parser was built into SeleniumBase to capture all lines from the specified desired capabilities file in the following formats:
``'KEY': 'VALUE'``
``caps['KEY'] = "VALUE"``
(Each pair must be on a separate line. You can interchange single and double quotes.)

You can also swap ``--browser=remote`` with an actual browser, eg ``--browser=chrome``, which will combine the default SeleniumBase desired capabilities with those that were specified in the capabilities file when using ``--cap_file=FILE.py``. (For example, you'll need default SeleniumBase desired capabilities when using a proxy server, which is not the same as the Selenium Grid server.)