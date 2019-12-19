## The Selenium Grid Hub

The Selenium Grid Hub lets you distribute tests to run in parallel across multiple node machines. Each node machine can then run its own allocation of tests. This allows you to run a large suite of tests very quickly.

### Running the Selenium Grid Hub

The following commands will work once you've installed seleniumbase.

#### <img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_box2.png" title="SeleniumBase" height="32"> Downloading the Selenium Server JAR file:
```
seleniumbase download server
```
* (Required for using your own Selenium Grid)

#### <img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_box2.png" title="SeleniumBase" height="32"> Grid Hub server controls:
```
seleniumbase grid-hub {start|stop|restart} [OPTIONS]
```
Options:
* ``-v``, ``--verbose``  (Increases verbosity of logging output.)

#### <img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_box2.png" title="SeleniumBase" height="32"> Grid node server controls:
```
seleniumbase grid-node {start|stop|restart} --hub=[HUB_IP] [OPTIONS]
```
Options:
* ``-v``, ``--verbose``  (Increases verbosity of logging output.)
* ``--hub=[HUB_IP]`` (Specifies the Grid Hub to connect to. Default: "127.0.0.1".)

When the Grid Hub Console is up and running, you'll be able to find it here: [http://127.0.0.1:4444/grid/console](http://127.0.0.1:4444/grid/console)

Now you can run your tests on the Selenium Grid:

```
pytest test_suite.py --server=IP_ADDRESS --port=4444
```

You can also run your tests on someone else's Selenium Grid to avoid managing your own. Here are some Selenium Grids that you can use (and the run command format):

* [BrowserStack](https://www.browserstack.com/automate#) Selenium Grid:
```
pytest my_first_test.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

* [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid:
```
pytest my_first_test.py --server=USERNAME:KEY@ondemand.saucelabs.com --port=80
```

* [TestingBot](https://testingbot.com/features) Selenium Grid:
```
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

(For setting browser desired capabilities while running Selenium remotely, see the ReadMe located here: https://github.com/seleniumbase/SeleniumBase/tree/master/examples/capabilities)

#### More info about the Selenium Grid Hub can be found here:
* [https://github.com/SeleniumHQ/selenium/wiki/Grid2](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
