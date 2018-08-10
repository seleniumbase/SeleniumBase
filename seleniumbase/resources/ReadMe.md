## Resources Help

SeleniumBase uses some Javascript libraries for optional advanced features such as website tours, messenger, highlighting elements on a page, and other jQuery actions. In some cases, you may want to host these Javascript and CSS files from your own websites. For simplicity and convenience, these resources have been downloaded into the "resources" folder. If you decide to use your local versions, you may need to update the corresponding URLs in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py).

Here are some of the resource files you'll find here:

**jquery.min.js** - This file is used by [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py) in activate_jquery(). The activate_jquery() method uses the version at [https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js](https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js). You only need this file if you're making jQuery calls in your automation (some base_case methods use jQuery).

**favicon.ico** - This file is used by [style_sheet.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/style_sheet.py) for the favicon icon. All it does is make the report page a little more professional-looking. Currently, SeleniumBase uses the version at [https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico](https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico).

**messenger/** - Files in this folder are used for creating Javascript notifications during test runs in Demo Mode.

**shepherd/** - Files in this folder are used for creating website tours using the Shepherd Javascript library.

**bootstrap_tour/** - Files in this folder are used for creating website tours using the Bootstrap Tour Javascript library. (SeleniumBase currently defaults to using Shepherd Tours.)
