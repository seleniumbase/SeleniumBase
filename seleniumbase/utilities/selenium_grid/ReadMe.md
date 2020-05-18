[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_q.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" height="30" /> The Selenium Grid Hub:

The Selenium Grid Hub lets you distribute tests to run in parallel across multiple node machines. Each node machine can then run its own allocation of tests. This allows you to run a large suite of tests very quickly.

### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" height="30" /> Running the Selenium Grid Hub:

The following commands will work once you've installed seleniumbase.

#### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" height="30" /> Downloading the Selenium Server JAR file:
```bash
seleniumbase download server
```
* (Required for using your own Selenium Grid)

#### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" height="30" /> Grid Hub server controls:
```bash
seleniumbase grid-hub {start|stop} [OPTIONS]
```
<b>Options:</b>
<ul>
<li> -v / --verbose  (Increases verbosity of logging output.)</li>
</ul>

#### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" height="30" /> Grid node server controls:
```bash
seleniumbase grid-node {start|stop} --hub=[HUB_IP] [OPTIONS]
```
<b>Options:</b>
<ul>
<li> -v / --verbose  (Increases verbosity of logging output.)</li>
<li> --hub=[HUB_IP]  (Specifies the Grid Hub to connect to. Default: "127.0.0.1".)</li>
</ul>

When the Grid Hub Console is up and running, you'll be able to find it here: [http://127.0.0.1:4444/grid/console](http://127.0.0.1:4444/grid/console)

Now you can run your tests on the Selenium Grid:

```bash
pytest test_suite.py --server=IP_ADDRESS --port=4444
```

You can also run your tests on someone else's Selenium Grid to avoid managing your own. Here are some Selenium Grids that you can use (and the run command format):

* [BrowserStack](https://www.browserstack.com/automate#) Selenium Grid:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

* [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid:
```bash
pytest my_first_test.py --server=USERNAME:KEY@ondemand.saucelabs.com --port=80
```

* [TestingBot](https://testingbot.com/features) Selenium Grid:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.testingbot.com --port=80
```

* [CrossBrowserTesting](https://help.crossbrowsertesting.com/selenium-testing/getting-started/python/) Selenium Grid:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.crossbrowsertesting.com --port=80
```

* [LambdaTest](https://www.lambdatest.com/selenium-automation) Selenium Grid:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.lambdatest.com --port=80
```

(For setting browser desired capabilities while running Selenium remotely, see the <a href="https://seleniumbase.io/help_docs/desired_capabilities/">desired capabilities documentation</a> and the sample files located in <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/capabilities">SeleniumBase/examples/capabilities</a>)

#### More info about the Selenium Grid Hub can be found here:
* [https://github.com/SeleniumHQ/selenium/wiki/Grid2](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
