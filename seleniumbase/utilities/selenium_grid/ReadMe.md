## The Selenium Grid Hub

The Selenium Grid Hub lets you distribute tests to run in parallel across multiple node machines. Each node machine can then run its own allocation of tests. This allows you to run a large suite of tests very quickly.

### Running the Selenium Grid Hub

The following commands will work once you've installed seleniumbase, which comes with the seleniumbase console scripts interface.

Grid Hub server controls:
```
seleniumbase grid-hub {start|stop|restart} [OPTIONS]
```
Options:
* ``-v``, ``--verbose``  (Increases verbosity of logging output.)

Grid node server controlls:
```
seleniumbase grid-node {start|stop|restart} --hub=[HUB_IP] [OPTIONS]
```
Options:
* ``-v``, ``--verbose``  (Increases verbosity of logging output.)
* ``--hub=[HUB_IP]`` (Specifies the Grid Hub to connect to. Default: "127.0.0.1".)

When the Grid Hub Console is up and running, you'll be able to find it here: [http://127.0.0.1:4444/grid/console](http://127.0.0.1:4444/grid/console)

Now you can run your tests on the Selenium Grid:

```
pytest my_test_suite.py --server=IP_ADDRESS --port=4444
```

You can also run your tests on [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid server (and not worry about managing your own Selenium Grid):

```
pytest my_first_test.py --server=username:key@hub.browserstack.com --port=80
```

And you can run your tests on the [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid server:

```
pytest my_first_test.py --server=username:key@ondemand.saucelabs.com --port=80
```


#### More info about the Selenium Grid Hub can be found here:
* [https://github.com/SeleniumHQ/selenium/wiki/Grid2](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
* [https://github.com/SeleniumHQ/selenium/wiki](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
