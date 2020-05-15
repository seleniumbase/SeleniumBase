## Using Safari's WebDriver for running browser tests on macOS

*(NOTE: Safari's WebDriver requires macOS 10.13 "High Sierra" or later.)*

You can find the official Apple documentation regarding "Testing with WebDriver in Safari" on the following page: [https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)

Run ``safaridriver --enable`` once in a terminal to enable Safari's WebDriver. (If you’re upgrading from a previous macOS release, you may need to prefix the command with ``sudo``.)

Now you can use ``--browser=safari`` to run your **SeleniumBase** tests on Safari.
