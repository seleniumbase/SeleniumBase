[<img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

[<img src="http://img.youtube.com/vi/Sjzq9kU5kOw/0.jpg" title="SeleniumBase Features" width="276">](https://www.youtube.com/watch?v=Sjzq9kU5kOw)
<p>(<b><a href="https://www.youtube.com/watch?v=Sjzq9kU5kOw">Watch the tutorial on YouTube</a></b>)</p>

<a id="feature_list"></a>
<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Features:</h2>

* A complete test automation framework for web/mobile UI testing.
* Uses [pytest](https://docs.pytest.org/en/latest/), [unittest](https://docs.python.org/3/library/unittest.html), and [nose](http://nose.readthedocs.io/en/latest/) for test discovery and execution.
* No more flaky tests! (Smart-waiting code keeps tests reliable.)
* Powerful [console scripts](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/console_scripts/ReadMe.md). (Type **``seleniumbase``** or **``sbase``** to use.)
* Has the ability to translate tests into [multiple spoken languages](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/translations).
* Has a flexible [command-line interface](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) for customizing test runs.
* Can run tests multithreaded in parallel. (Use ``-n NUM_THREADS``)
* Has [Plugins](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/plugins) for logging data and screenshots. ([Click to learn more](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md))
* Has a [global config file](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) for configuring SeleniumBase as needed.
* Includes a [website tour builder](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md) for creating interactive walkthroughs.
* Includes a tool for [creating interactive web presentations](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/ReadMe.md).
* Includes [Chart Maker](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/chart_maker/ReadMe.md), a tool for creating interactive charts.
* Backwards-compatible with [WebDriver](https://www.selenium.dev/projects/). (Use ``self.driver`` anywhere.)
* Includes code to [export Katalon Recorder scripts into SeleniumBase format](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/katalon/ReadMe.md).
* Can run tests in Headless Mode to hide the web browser. (Use ``--headless``)
* Can run tests through a proxy server. (Use ``--proxy=IP_ADDRESS:PORT``)
* Can use an authenticated proxy server. (``--proxy=USER:PASS@IP_ADDRESS:PORT``)
* Can change the web browser's user agent string. (Use ``--agent=USER_AGENT_STRING``)
* Can run tests using Chrome's mobile device emulator (Use ``--mobile``)
* Can set a Chrome User Data Directory / Profile to load. (Use ``--user_data_dir=DIR``)
* Can load Chrome Extension ZIP files. (Use ``--extension_zip=ZIP``)
* Can load Chrome Extension folders. (Use ``--extension_dir=DIR``)
* Can handle Google Authenticator logins with [Python's one-time password library](https://pyotp.readthedocs.io/en/latest/).
* Includes a hybrid-automation solution called [MasterQA](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md) to speed up manual testing.
* Integrates with [MySQL](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/testcase_manager.py), [Selenium Grid](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), [Azure](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md), [Google Cloud](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/google_cloud/ReadMe.md), [AWS](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/s3_logging_plugin.py), and [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md).
* Can connect to [BrowserStack](https://www.browserstack.com/automate#), [Sauce Labs](https://saucelabs.com/products/web-testing/cross-browser-testing), or [TestingBot](https://testingbot.com/features) Selenium Grids.
* Includes a tool for [converting Selenium IDE recordings](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_ide) into SeleniumBase scripts.
* Can load and make assertions on PDF files from websites or the local file system.
* Can reuse the same Selenium browser session between tests. (Use: ``--reuse-session``)
* Written in Python, but can also make JavaScript calls. (Use: ``self.execute_script()``)
* Includes useful [Python decorators and password obfuscation methods](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/ReadMe.md).

[<img src="https://seleniumbase.io/cdn/img/super_logo_3.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
