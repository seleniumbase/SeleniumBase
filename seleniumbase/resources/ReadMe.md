## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Resources Help

SeleniumBase uses some Javascript libraries for optional advanced features such as website tours, messenger, highlighting elements on a page, and other jQuery actions. In some cases, you may want to host these Javascript and CSS files from your own websites. For simplicity and convenience, these resources have been downloaded into the "resources" folder. If you decide to use your local versions, you may need to update the corresponding URLs in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py).

Here are some of the resource files you'll find here:

**favicon.ico** - This file is used by [style_sheet.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/style_sheet.py) for the favicon icon. Currently, SeleniumBase uses the version at [https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico](https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/resources/favicon.ico).

**messenger/** - Files in this folder are used for creating Javascript notifications during test runs in Demo Mode.

**jquery_confirm/** - Files in this folder are used for creating Javascript confirmation prompts during test runs when using MasterQA.

**shepherd/** - Files in this folder are used for creating website tours using the Shepherd Javascript library. (This is the default tour library.)

**bootstrap_tour/** - Files in this folder are used for creating website tours using the Bootstrap Tour Javascript library.

**introjs/** - Files in this folder are used for creating website tours using the IntroJS Javascript library.

**hopscotch/** - Files in this folder are used for creating website tours using the Hopscotch Javascript library.
