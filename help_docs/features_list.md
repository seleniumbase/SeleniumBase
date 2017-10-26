<a id="feature_list"></a>
### ![http://seleniumbase.com](https://cdn2.hubspot.net/hubfs/100006/images/super_logo_tiny.png "SeleniumBase") **SeleniumBase Features:**
* A versatile test automation framework for building & running Selenium scripts reliably.
* Uses [Pytest](https://docs.pytest.org/en/latest/) and [Nose](http://nose.readthedocs.io/en/latest/) for test discovery and for gathering detailed stacktrace info.
* Can run tests locally, from [Jenkins](https://jenkins.io/) headlessly, or remotely with [Selenium Grid](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/selenium_grid).
* Uses a flexible command line interface to customize & control test runs.
* Has [Python libraries](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase) for helping you do more with Selenium-WebDriver.
* Has [Plugins](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/plugins) for logging data and screenshots automatically. ([Click to learn how](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md))
* Uses a [global config file](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) to make SeleniumBase unique to your specific environment needs.
* Backwards-compatible with [WebDriver](http://www.seleniumhq.org/projects/webdriver/). (Use ``self.driver`` anywhere.)
* Includes a hybrid-automation solution called **[MasterQA](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md)** to speed up manual testing.
* Includes integrations with [MySQL](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/testcase_manager.py), [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md), [Google Cloud](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/google_cloud/ReadMe.md), [Amazon S3](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/s3_logging_plugin.py), and [NodeJS](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/node_js).
* Includes a [tool to convert Selenium IDE recordings](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/selenium_ide) into clean & robust SeleniumBase scripts.
* Written in Python, but can also make JavaScript calls using ``self.execute_script()``.
* Includes useful Python decorators and password obfuscation methods. ([Learn more here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/ReadMe.md))
