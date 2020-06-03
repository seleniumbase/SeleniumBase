## <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Resources Help

SeleniumBase uses some JavaScript libraries for optional advanced features such as website tours, messenger, HTML validation, highlighting elements on a page, and other jQuery actions. In some cases, you may want to host these JavaScript and CSS files from your own websites. For simplicity and convenience, these resources have been downloaded into the "resources" folder. If you decide to use your local versions, you may need to update the corresponding URLs in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py).

Here are some of the resource files you'll find here:

**favicon.ico** - This file is used by [style_sheet.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/style_sheet.py) for the favicon icon. Currently, SeleniumBase uses the version at [https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico](https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico).

**messenger/** - Files in this folder are used for creating JavaScript notifications during test runs in Demo Mode.

**jquery_confirm/** - Files in this folder are used for creating JavaScript confirmation prompts during test runs when using MasterQA.

**html_inspector/** - Files in this folder are used for the HTML Inspector, which validates website pages.

**shepherd/** - Files in this folder are used for creating website tours using the Shepherd JavaScript library. (This is the default tour library.)

**bootstrap_tour/** - Files in this folder are used for creating website tours using the Bootstrap Tour JavaScript library.

**introjs/** - Files in this folder are used for creating website tours using the IntroJS JavaScript library.

**driverjs/** - Files in this folder are used for creating website tours using the DriverJS JavaScript library.

**hopscotch/** - Files in this folder are used for creating website tours using the Hopscotch JavaScript library.
