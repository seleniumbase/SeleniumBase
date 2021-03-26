<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Resource Files</h2>

SeleniumBase uses JavaScript libraries for bonus features such as the Website Tour Maker, Presentation Maker, Chart Maker, Demo Mode, HTML Inspector, and more. In general, SeleniumBase retrieves these resources via CDN link. In some cases, you may want to host these JavaScript and CSS files from your own CDN. For simplicity and convenience, some of these resources have been downloaded into the "resources" folder. If you decide to use your own CDN, you may need to update links in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py) and [constants.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/constants.py).

Here are some of the resource files you'll find here:

**favicon.ico** - This file is used by [style_sheet.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/style_sheet.py) for the favicon icon. Currently, SeleniumBase uses the version at [https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico](https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico).

**messenger/** - Files in this folder are used for creating JavaScript notifications during test runs in Demo Mode.

**jquery_confirm/** - Files in this folder are used for creating JavaScript confirmation prompts during test runs when using MasterQA.

**html_inspector/** - Files in this folder are used for the HTML Inspector, which validates website pages.

--------

The remaining resources have been moved into [github.com/seleniumbase/resource-files](https://github.com/seleniumbase/resource-files) in order to reduce the size of SeleniumBase:

**reveal/** - Files in this folder are used for the HTML Presentation Maker.

**prettify/** - Files in this folder are used to assist the HTML Presentation Maker.

**shepherd/** - Files in this folder are used for creating website tours using the Shepherd JavaScript library.

**bootstrap_tour/** - Files in this folder are used for creating website tours using the Bootstrap Tour JavaScript library.

**introjs/** - Files in this folder are used for creating website tours using the IntroJS JavaScript library.

**driverjs/** - Files in this folder are used for creating website tours using the DriverJS JavaScript library.

**hopscotch/** - Files in this folder are used for creating website tours using the Hopscotch JavaScript library.
