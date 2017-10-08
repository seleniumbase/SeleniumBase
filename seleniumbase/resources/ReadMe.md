## Resources Help

If you want to run SeleniumBase automation on local web pages while offline, that's possible if you copy the resource files here to a location where your local web server is able to access those files as long as you make the necessary updates to your local copy of SeleniumBase. You might not even need to use them depending on what you're doing.

**jquery-3.2.1.min.js** - This file is used by [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py) in activate_jquery(). The activate_jquery() method uses the version at [http://code.jquery.com/jquery-3.2.1.min.js](http://code.jquery.com/jquery-3.2.1.min.js). You only need this file if you're making jQuery calls in your automation (some base_case methods use jQuery).

**favicon.ico** - This file is used by [style_sheet.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/style_sheet.py) for the favicon icon. All it does is make the report page a little more professional-looking. Currently, SeleniumBase uses the version at [https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico](https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico).
