[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_i.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

[<img src="http://img.youtube.com/vi/Sjzq9kU5kOw/0.jpg" title="SeleniumBase" height="180">](https://www.youtube.com/watch?v=Sjzq9kU5kOw)

(**[Watch an overview on YouTube](https://www.youtube.com/watch?v=Sjzq9kU5kOw)**)

<a id="feature_list"></a>
## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Features:**
* A complete test automation framework for building & running reliable testing scripts.
* Uses [Pytest](https://docs.pytest.org/en/latest/) or [Nose](http://nose.readthedocs.io/en/latest/) runners for test discovery, organization, execution, and logging.
* Includes [console scripts](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/console_scripts/ReadMe.md) that save you time by installing web drivers automatically, etc. 
* Includes a [website tour builder](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md) for creating and running walkthroughs on any website.
* Works on multiple platforms such as macOS, Windows, Linux, and [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md).
* Uses a [flexible command-line interface](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) to customize & configure test runs.
* Can run tests using multiple concurrent threads. (Use ``-n THREAD_COUNT``)
* Has Python libraries for helping you do much more with Selenium/WebDriver.
* Has [Plugins](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/plugins) for logging data and screenshots automatically. ([Click to learn more](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md))
* Uses a [global config file](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) for configuring SeleniumBase to your specific needs.
* Backwards-compatible with [WebDriver](http://www.seleniumhq.org/projects/webdriver/). (Use ``self.driver`` anywhere.)
* Can run tests in Headless Mode to hide the web browser. (Use ``--headless``)
* Can run tests through a proxy server. (Use ``--proxy=IP_ADDRESS:PORT``)
* Can use an authenticated proxy server. (``--proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT``)
* Can change the web browser's user agent string. (Use ``--agent=USER_AGENT_STRING``)
* Can run tests using Chrome's mobile device emulator (Use ``--mobile``)
* Can set a Chrome User Data Directory / Profile to load. (Use ``--user_data_dir=DIR``)
* Can load Chrome Extension ZIP files (comma-separated). (Use ``--extension_zip=ZIP``)
* Can load Chrome Extension folders (comma-separated). (Use ``--extension_dir=DIR``)
* Can handle Google Authenticator logins by using the [Python one-time password library](https://pyotp.readthedocs.io/en/latest/).
* Includes a hybrid-automation solution called **[MasterQA](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md)** to speed up manual testing.
* Integrates with [MySQL](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/testcase_manager.py), [Selenium Grid](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), [Azure](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md), [Google Cloud](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/google_cloud/ReadMe.md), [Amazon S3](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/s3_logging_plugin.py), and [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md).
* Has the ability to connect to a [BrowserStack](https://www.browserstack.com/automate#), [Sauce Labs](https://saucelabs.com/products/web-testing/cross-browser-testing), or [TestingBot](https://testingbot.com/features) Selenium Grid.
* Includes a [tool to convert Selenium IDE recordings](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_ide) into clean, robust SeleniumBase scripts.
* Can load and make assertions on PDF files from websites or the local file system.
* Can reuse the same Selenium browser session between tests. (Use: ``--reuse-session``)
* Written in Python, but can also make JavaScript calls. (Use: ``self.execute_script()``)
* Includes useful Python decorators and password obfuscation methods. ([Learn more here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/ReadMe.md))
