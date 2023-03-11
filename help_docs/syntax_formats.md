<!-- SeleniumBase Docs -->

<a id="syntax_formats"></a>

## [<img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="40">](https://github.com/seleniumbase/SeleniumBase/) The 23 Syntax Formats

<h3><b>SeleniumBase</b> currently supports 23 unique syntax formats (<i>"design patterns"</i>) for structuring tests.</h3>

--------

<blockquote>
<p dir="auto"><strong>Table of Contents / Navigation:</strong></p>
<ul dir="auto">
<li><a href="#sb_sf_01"><strong>01. BaseCase direct class inheritance</strong></a></li>
<li><a href="#sb_sf_02"><strong>02. BaseCase subclass inheritance</strong></a></li>
<li><a href="#sb_sf_03"><strong>03. The "sb" pytest fixture (no class)</strong></a></li>
<li><a href="#sb_sf_04"><strong>04. The "sb" pytest fixture (in class)</strong></a></li>
<li><a href="#sb_sf_05"><strong>05. Page Object Model with BaseCase</strong></a></li>
<li><a href="#sb_sf_06"><strong>06. Page Object Model with the "sb" fixture</strong></a></li>
<li><a href="#sb_sf_07"><strong>07. Using "request" to get "sb" (no class)</strong></a></li>
<li><a href="#sb_sf_08"><strong>08. Using "request" to get "sb" (in class)</strong></a></li>
<li><a href="#sb_sf_09"><strong>09. Overriding the driver via BaseCase</strong></a></li>
<li><a href="#sb_sf_10"><strong>10. Overriding the driver via "sb" fixture</strong></a></li>
<li><a href="#sb_sf_11"><strong>11. BaseCase with Chinese translations</strong></a></li>
<li><a href="#sb_sf_12"><strong>12. BaseCase with Dutch translations</strong></a></li>
<li><a href="#sb_sf_13"><strong>13. BaseCase with French translations</strong></a></li>
<li><a href="#sb_sf_14"><strong>14. BaseCase with Italian translations</strong></a></li>
<li><a href="#sb_sf_15"><strong>15. BaseCase with Japanese translations</strong></a></li>
<li><a href="#sb_sf_16"><strong>16. BaseCase with Korean translations</strong></a></li>
<li><a href="#sb_sf_17"><strong>17. BaseCase with Portuguese translations</strong></a></li>
<li><a href="#sb_sf_18"><strong>18. BaseCase with Russian translations</strong></a></li>
<li><a href="#sb_sf_19"><strong>19. BaseCase with Spanish translations</strong></a></li>
<li><a href="#sb_sf_20"><strong>20. Gherkin syntax with "behave" BDD runner</strong></a></li>
<li><a href="#sb_sf_21"><strong>21. SeleniumBase SB (Python context manager)</strong></a></li>
<li><a href="#sb_sf_22"><strong>22. The driver manager (via context manager)</strong></a></li>
<li><a href="#sb_sf_23"><strong>23. The driver manager (via direct import)</strong></a></li>
</ul>
</blockquote>

--------

<a id="sb_sf_01"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 1. BaseCase direct class inheritance</h3>

In this format, (which is used by most of the tests in the <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples">SeleniumBase examples folder</a>), <code>BaseCase</code> is imported at the top of a Python file, followed by a Python class inheriting <code>BaseCase</code>. Then, any test method defined in that class automatically gains access to SeleniumBase methods, including the <code>setUp()</code> and <code>tearDown()</code> methods that are automatically called for opening and closing web browsers at the start and end of tests.

To run a test of this format, use **``pytest``** or ``nosetests``. Adding ``BaseCase.main(__name__, __file__)`` enables ``python`` to run ``pytest`` on your file indirectly. Here's an example:

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class MyTestClass(BaseCase):
    def test_demo_site(self):
        self.open("https://seleniumbase.io/demo_page")
        self.type("#myTextInput", "This is Automated")
        self.click("#myButton")
        self.assert_element("tbody#tbodyId")
        self.assert_text("Automation Practice", "h3")
        self.click_link("SeleniumBase Demo Page")
        self.assert_exact_text("Demo Page", "h1")
        self.assert_no_js_errors()
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py">examples/test_demo_site.py</a> for the full test.)

Using ``BaseCase`` inheritance is a great starting point for anyone learning SeleniumBase, and it follows good object-oriented programming principles.

<a id="sb_sf_02"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 2. BaseCase subclass inheritance</h3>

There are situations where you may want to customize the <code>setUp</code> and <code>tearDown</code> of your tests. Maybe you want to have all your tests login to a specific web site first, or maybe you want to have your tests report results through an API call depending on whether a test passed or failed. <b>This can be done by creating a subclass of <code>BaseCase</code> and then carefully creating custom <code>setUp()</code> and <code>tearDown()</code> methods that don't overwrite the critical functionality of the default SeleniumBase <code>setUp()</code> and <code>tearDown()</code> methods.</b> Afterwards, your test classes will inherit the subclass of <code>BaseCase</code> with the added functionality, rather than directly inheriting <code>BaseCase</code> itself. Here's an example of that:

```python
from seleniumbase import BaseCase

class BaseTestCase(BaseCase):
    def setUp(self):
        super().setUp()
        # <<< Run custom setUp() code for tests AFTER the super().setUp() >>>

    def tearDown(self):
        self.save_teardown_screenshot()  # On failure or "--screenshot"
        if self.has_exception():
            # <<< Run custom code if the test failed. >>>
            pass
        else:
            # <<< Run custom code if the test passed. >>>
            pass
        # (Wrap unreliable tearDown() code in a try/except block.)
        # <<< Run custom tearDown() code BEFORE the super().tearDown() >>>
        super().tearDown()

    def login(self):
        # <<< Placeholder. Add your code here. >>>
        # Reduce duplicate code in tests by having reusable methods like this.
        # If the UI changes, the fix can be applied in one place.
        pass

    def example_method(self):
        # <<< Placeholder. Add your code here. >>>
        pass

class MyTests(BaseTestCase):
    def test_example(self):
        self.login()
        self.example_method()
        self.type("input", "Name")
        self.click("form button")
        ...
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/boilerplates/base_test_case.py">examples/boilerplates/base_test_case.py</a> for more info.)

<a id="sb_sf_03"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 3. The "sb" pytest fixture (no class)</h3>

The pytest framework comes with a unique system called fixtures, which replaces import statements at the top of Python files by importing libraries directly into test definitions. More than just being an import, a pytest fixture can also automatically call predefined <code>setUp()</code> and <code>tearDown()</code> methods at the beginning and end of test methods. To work, <code>sb</code> is added as an argument to each test method definition that needs SeleniumBase functionality. This means you no longer need import statements in your Python files to use SeleniumBase. <b>If using other pytest fixtures in your tests, you may need to use the SeleniumBase fixture (instead of <code>BaseCase</code> class inheritance) for compatibility reasons.</b> Here's an example of the <code>sb</code> fixture in a test that does not use Python classes:

```python
def test_sb_fixture_with_no_class(sb):
    sb.open("https://google.com/ncr")
    sb.type('input[title="Search"]', 'SeleniumBase\n')
    sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
    sb.click('a[title="seleniumbase"]')
```

(See the top of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_sb_fixture.py">examples/test_sb_fixture.py</a> for the test.)

<a id="sb_sf_04"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 4. The "sb" pytest fixture (in class)</h3>

The <code>sb</code> pytest fixture can also be used inside of a class. There is a slight change to the syntax because that means test methods must also include <code>self</code> in their argument definitions when test methods are defined. (The <code>self</code> argument represents the class object, and is used in every test method that lives inside of a class.) Once again, no import statements are needed in your Python files for this to work. Here's an example of using the <code>sb</code> fixture in a test method that lives inside of a Python class:

```python
class Test_SB_Fixture:
    def test_sb_fixture_inside_class(self, sb):
        sb.open("https://google.com/ncr")
        sb.type('input[title="Search"]', 'SeleniumBase\n')
        sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
        sb.click('a[title="examples"]')
```

(See the bottom of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_sb_fixture.py">examples/test_sb_fixture.py</a> for the test.)

<a id="sb_sf_05"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 5. Page Object Model with BaseCase</h3>

With SeleniumBase, you can use Page Objects to break out code from tests, but remember, the <code>self</code> variable (from test methods that inherit <code>BaseCase</code>) contains the driver and all other framework-specific variable definitions. Therefore, that <code>self</code> must be passed as an arg into any outside class method in order to call SeleniumBase methods from there. In the example below, the <code>self</code> variable from the test method is passed into the <code>sb</code> arg of the Page Object class method because the <code>self</code> arg of the Page Object class method is already being used for its own class. Every Python class method definition must include the <code>self</code> as the first arg.

```python
from seleniumbase import BaseCase

class LoginPage:
    def login_to_swag_labs(self, sb, username):
        sb.open("https://www.saucedemo.com")
        sb.type("#user-name", username)
        sb.type("#password", "secret_sauce")
        sb.click('input[type="submit"]')

class MyTests(BaseCase):
    def test_swag_labs_login(self):
        LoginPage().login_to_swag_labs(self, "standard_user")
        self.assert_element("div.inventory_list")
        self.assert_element('div:contains("Sauce Labs Backpack")')
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/boilerplates/samples/swag_labs_test.py">examples/boilerplates/samples/swag_labs_test.py</a> for the full test.)

<a id="sb_sf_06"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 6. Page Object Model with the "sb" fixture</h3>

This is similar to the classic Page Object Model with <code>BaseCase</code> inheritance, except that this time we pass the <code>sb</code> pytest fixture from the test into the <code>sb</code> arg of the page object class method, (instead of passing <code>self</code>). Now that you're using <code>sb</code> as a pytest fixture, you no longer need to import <code>BaseCase</code> anywhere in your code. See the example below:

```python
class LoginPage:
    def login_to_swag_labs(self, sb, username):
        sb.open("https://www.saucedemo.com")
        sb.type("#user-name", username)
        sb.type("#password", "secret_sauce")
        sb.click('input[type="submit"]')

class MyTests:
    def test_swag_labs_login(self, sb):
        LoginPage().login_to_swag_labs(sb, "standard_user")
        sb.assert_element("div.inventory_list")
        sb.assert_element('div:contains("Sauce Labs Backpack")')
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/boilerplates/samples/sb_swag_test.py">examples/boilerplates/samples/sb_swag_test.py</a> for the full test.)

<a id="sb_sf_07"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 7. Using "request" to get "sb" (no class)</h3>

The pytest <code>request</code> fixture can be used to retrieve other pytest fixtures from within tests, such as the <code>sb</code> fixture. This allows you to have more control over when fixtures get initialized because the fixture no longer needs to be loaded at the very beginning of test methods. This is done by calling <code>request.getfixturevalue('sb')</code> from the test. Here's an example of using the pytest <code>request</code> fixture to load the <code>sb</code> fixture in a test method that does not use Python classes:

```python
def test_request_sb_fixture(request):
    sb = request.getfixturevalue('sb')
    sb.open("https://seleniumbase.io/demo_page")
    sb.assert_text("SeleniumBase", "#myForm h2")
    sb.assert_element("input#myTextInput")
    sb.type("#myTextarea", "This is me")
    sb.click("#myButton")
    sb.tearDown()
```

(See the top of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_request_sb_fixture.py">examples/test_request_sb_fixture.py</a> for the test.)

<a id="sb_sf_08"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 8. Using "request" to get "sb" (in class)</h3>

The pytest <code>request</code> fixture can also be used to get the <code>sb</code> fixture from inside a Python class. Here's an example of that:

```python
class Test_Request_Fixture:
    def test_request_sb_fixture_in_class(self, request):
        sb = request.getfixturevalue('sb')
        sb.open("https://seleniumbase.io/demo_page")
        sb.assert_element("input#myTextInput")
        sb.type("#myTextarea", "Automated")
        sb.assert_text("This Text is Green", "#pText")
        sb.click("#myButton")
        sb.assert_text("This Text is Purple", "#pText")
        sb.tearDown()
```

(See the bottom of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_request_sb_fixture.py">examples/test_request_sb_fixture.py</a> for the test.)

<a id="sb_sf_09"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 9. Overriding the driver via BaseCase</h3>

When you want to use SeleniumBase methods via <code>BaseCase</code>, but you want total freedom to control how you spin up your web browsers, this is the format you want. Although SeleniumBase gives you plenty of command-line options to change how your browsers are launched, this format gives you more control when the existing options aren't enough. Here's an example of that:

```python
from selenium import webdriver
from seleniumbase import BaseCase

class OverrideDriverTest(BaseCase):
    def get_new_driver(self, *args, **kwargs):
        """This method overrides get_new_driver() from BaseCase."""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-3d-apis")
        options.add_argument("--disable-notifications")
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"],
        )
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=options)

    def test_simple(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_text("Demo Page", "h1")
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_override_driver.py">examples/test_override_driver.py</a>)

The above format lets you customize [selenium-wire](https://github.com/wkeeling/selenium-wire) for intercepting and inspecting requests and responses during SeleniumBase tests. Here's how a ``selenium-wire`` integration may look:

```python
from seleniumbase import BaseCase
from seleniumwire import webdriver  # Requires "pip install selenium-wire"


class WireTestCase(BaseCase):
    def get_new_driver(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_experimental_option("useAutomationExtension", False)
        return webdriver.Chrome(options=options)

    def test_simple(self):
        self.open("https://seleniumbase.io/demo_page")
        for request in self.driver.requests:
            print(request.url)
```

(NOTE: The ``selenium-wire`` integration is now included with ``seleniumbase``: Add ``--wire`` as a ``pytest`` command-line option to activate.)

<a id="sb_sf_10"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 10. Overriding the driver via "sb" fixture</h3>

When you want to use SeleniumBase methods via the ``sb`` pytest fixture, but you want total freedom to control how you spin up your web browsers, this is the format you want. Although SeleniumBase gives you plenty of command-line options to change how your browsers are launched, this format gives you more control when the existing options aren't enough.

```python
"""Overriding the "sb" fixture to override the driver."""
import pytest

@pytest.fixture()
def sb(request):
    from selenium import webdriver
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def get_new_driver(self, *args, **kwargs):
            """This method overrides get_new_driver() from BaseCase."""
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"],
            )
            return webdriver.Chrome(options=options)

        def setUp(self):
            super().setUp()

        def base_method(self):
            pass

        def tearDown(self):
            self.save_teardown_screenshot()  # On failure or "--screenshot"
            super().tearDown()

    sb = BaseClass("base_method")
    sb.setUpClass()
    sb.setUp()
    yield sb
    sb.tearDown()
    sb.tearDownClass()

def test_override_fixture_no_class(sb):
    sb.open("https://seleniumbase.io/demo_page")
    sb.type("#myTextInput", "This is Automated")

class TestOverride:
    def test_override_fixture_inside_class(self, sb):
        sb.open("https://seleniumbase.io/demo_page")
        sb.type("#myTextInput", "This is Automated")
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_override_sb_fixture.py">examples/test_override_sb_fixture.py</a>)

Here's how the [selenium-wire](https://github.com/wkeeling/selenium-wire) integration may look when overriding the ``sb`` pytest fixture to override the driver:

```python
import pytest

@pytest.fixture()
def sb(request):
    import sys
    from seleniumbase import BaseCase
    from seleniumwire import webdriver  # Requires "pip install selenium-wire"

    class BaseClass(BaseCase):
        def get_new_driver(self, *args, **kwargs):
            options = webdriver.ChromeOptions()
            if "linux" in sys.platform:
                options.add_argument("--headless=new")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"],
            )
            return webdriver.Chrome(options=options)

        def setUp(self):
            super().setUp()

        def tearDown(self):
            self.save_teardown_screenshot()  # On failure or "--screenshot"
            super().tearDown()

        def base_method(self):
            pass

    sb = BaseClass("base_method")
    sb.setUpClass()
    sb.setUp()
    yield sb
    sb.tearDown()
    sb.tearDownClass()

def test_wire_with_no_class(sb):
    sb.open("https://seleniumbase.io/demo_page")
    for request in sb.driver.requests:
        print(request.url)

class TestWire:
    def test_wire_inside_class(self, sb):
        sb.open("https://seleniumbase.io/demo_page")
        for request in sb.driver.requests:
            print(request.url)
```

(NOTE: The ``selenium-wire`` integration is now included with ``seleniumbase``: Add ``--wire`` as a ``pytest`` command-line option to activate. If you need both ``--wire`` with ``--undetected`` modes together, you'll still need to override ``get_new_driver()``.)

<a id="sb_sf_11"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 11. BaseCase with Chinese translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Chinese. Here's an example of that:

```python
from seleniumbase.translate.chinese import 硒测试用例
硒测试用例.main(__name__, __file__)


class 我的测试类(硒测试用例):
    def test_例子1(self):
        self.开启("https://zh.wikipedia.org/wiki/")
        self.断言标题("维基百科，自由的百科全书")
        self.断言元素('a[title="首页"]')
        self.断言文本("新闻动态", "span#新闻动态")
        self.输入文本("#searchInput", "舞龍")
        self.单击("#searchButton")
        self.断言文本("舞龍", "#firstHeading")
        self.断言元素('img[src*="Chinese_draak.jpg"]')
        self.输入文本("#searchInput", "麻婆豆腐")
        self.单击("#searchButton")
        self.断言文本("麻婆豆腐", "#firstHeading")
        self.断言元素('div.thumb div:contains("一家中餐館的麻婆豆腐")')
        self.输入文本("#searchInput", "精武英雄")
        self.单击("#searchButton")
        self.断言元素('img[src*="Fist_of_legend.jpg"]')
        self.断言文本("李连杰", 'li a[title="李连杰"]')
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/chinese_test_1.py">examples/translations/chinese_test_1.py</a> for the Chinese test.)

<a id="sb_sf_12"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 12. BaseCase with Dutch translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Dutch. Here's an example of that:

```python
from seleniumbase.translate.dutch import Testgeval
Testgeval.main(__name__, __file__)


class MijnTestklasse(Testgeval):
    def test_voorbeeld_1(self):
        self.openen("https://nl.wikipedia.org/wiki/Hoofdpagina")
        self.controleren_element('a[title*="hoofdpagina gaan"]')
        self.controleren_tekst("Welkom op Wikipedia", "td.hp-welkom")
        self.typ("#searchInput", "Stroopwafel")
        self.klik("#searchButton")
        self.controleren_tekst("Stroopwafel", "#firstHeading")
        self.controleren_element('img[src*="Stroopwafels"]')
        self.typ("#searchInput", "Rijksmuseum Amsterdam")
        self.klik("#searchButton")
        self.controleren_tekst("Rijksmuseum", "#firstHeading")
        self.controleren_element('img[src*="Rijksmuseum"]')
        self.terug()
        self.controleren_url_bevat("Stroopwafel")
        self.vooruit()
        self.controleren_url_bevat("Rijksmuseum")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/dutch_test_1.py">examples/translations/dutch_test_1.py</a> for the Dutch test.)

<a id="sb_sf_13"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 13. BaseCase with French translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into French. Here's an example of that:

```python
from seleniumbase.translate.french import CasDeBase
CasDeBase.main(__name__, __file__)


class MaClasseDeTest(CasDeBase):
    def test_exemple_1(self):
        self.ouvrir("https://fr.wikipedia.org/wiki/")
        self.vérifier_texte("Wikipédia")
        self.vérifier_élément('[alt="Wikipédia"]')
        self.js_taper("#searchform input", "Crème brûlée")
        self.cliquer("#searchform button")
        self.vérifier_texte("Crème brûlée", "#firstHeading")
        self.vérifier_élément('img[alt*="Crème brûlée"]')
        self.js_taper("#searchform input", "Jardin des Tuileries")
        self.cliquer("#searchform button")
        self.vérifier_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_url_contient("brûlée")
        self.en_avant()
        self.vérifier_url_contient("Jardin")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/french_test_1.py">examples/translations/french_test_1.py</a> for the French test.)

<a id="sb_sf_14"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 14. BaseCase with Italian translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Italian. Here's an example of that:

```python
from seleniumbase.translate.italian import CasoDiProva
CasoDiProva.main(__name__, __file__)


class MiaClasseDiTest(CasoDiProva):
    def test_esempio_1(self):
        self.apri("https://it.wikipedia.org/wiki/")
        self.verificare_testo("Wikipedia")
        self.verificare_elemento('a[title="Lingua italiana"]')
        self.digitare("#searchInput", "Pizza")
        self.fare_clic("#searchButton")
        self.verificare_testo("Pizza", "#firstHeading")
        self.verificare_elemento('figure img[src*="pizza"]')
        self.digitare("#searchInput", "Colosseo")
        self.fare_clic("#searchButton")
        self.verificare_testo("Colosseo", "#firstHeading")
        self.verificare_elemento('figure img[src*="Colosseo"]')
        self.indietro()
        self.verificare_url_contiene("Pizza")
        self.avanti()
        self.verificare_url_contiene("Colosseo")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/italian_test_1.py">examples/translations/italian_test_1.py</a> for the Italian test.)

<a id="sb_sf_15"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 15. BaseCase with Japanese translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Japanese. Here's an example of that:

```python
from seleniumbase.translate.japanese import セレニウムテストケース
セレニウムテストケース.main(__name__, __file__)


class 私のテストクラス(セレニウムテストケース):
    def test_例1(self):
        self.を開く("https://ja.wikipedia.org/wiki/")
        self.テキストを確認する("ウィキペディア")
        self.要素を確認する('[title*="ウィキペディアへようこそ"]')
        self.JS入力('input[name="search"]', "アニメ")
        self.クリックして("#searchform button")
        self.テキストを確認する("アニメ", "#firstHeading")
        self.JS入力('input[name="search"]', "寿司")
        self.クリックして("#searchform button")
        self.テキストを確認する("寿司", "#firstHeading")
        self.要素を確認する('img[alt="握り寿司"]')
        self.JS入力("#searchInput", "レゴランド・ジャパン")
        self.クリックして("#searchform button")
        self.要素を確認する('img[alt*="LEGOLAND JAPAN"]')
        self.リンクテキストを確認する("名古屋城")
        self.リンクテキストをクリックします("テーマパーク")
        self.テキストを確認する("テーマパーク", "#firstHeading")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/japanese_test_1.py">examples/translations/japanese_test_1.py</a> for the Japanese test.)

<a id="sb_sf_16"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 16. BaseCase with Korean translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Korean. Here's an example of that:

```python
from seleniumbase.translate.korean import 셀레늄_테스트_케이스
셀레늄_테스트_케이스.main(__name__, __file__)


class 테스트_클래스(셀레늄_테스트_케이스):
    def test_실시예_1(self):
        self.열기("https://ko.wikipedia.org/wiki/")
        self.텍스트_확인("위키백과")
        self.요소_확인('[title="위키백과:소개"]')
        self.JS_입력("#searchform input", "김치")
        self.클릭("#searchform button")
        self.텍스트_확인("김치", "#firstHeading")
        self.요소_확인('img[alt="Various kimchi.jpg"]')
        self.링크_텍스트_확인("한국 요리")
        self.JS_입력("#searchform input", "비빔밥")
        self.클릭("#searchform button")
        self.텍스트_확인("비빔밥", "#firstHeading")
        self.요소_확인('img[alt="Dolsot-bibimbap.jpg"]')
        self.링크_텍스트를_클릭합니다("돌솥비빔밥")
        self.텍스트_확인("돌솥비빔밥", "#firstHeading")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/korean_test_1.py">examples/translations/korean_test_1.py</a> for the Korean test.)

<a id="sb_sf_17"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 17. BaseCase with Portuguese translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Portuguese. Here's an example of that:

```python
from seleniumbase.translate.portuguese import CasoDeTeste
CasoDeTeste.main(__name__, __file__)


class MinhaClasseDeTeste(CasoDeTeste):
    def test_exemplo_1(self):
        self.abrir("https://pt.wikipedia.org/wiki/")
        self.verificar_texto("Wikipédia")
        self.verificar_elemento('[title="Língua portuguesa"]')
        self.digitar("#searchform input", "João Pessoa")
        self.clique("#searchform button")
        self.verificar_texto("João Pessoa", "#firstHeading")
        self.verificar_elemento('img[alt*="João Pessoa"]')
        self.digitar("#searchform input", "Florianópolis")
        self.clique("#searchform button")
        self.verificar_texto("Florianópolis", "h1#firstHeading")
        self.verificar_elemento('td:contains("Avenida Beira-Mar")')
        self.voltar()
        self.verificar_url_contém("João_Pessoa")
        self.atualizar_a_página()
        self.js_digitar("#searchform input", "Teatro Amazonas")
        self.clique("#searchform button")
        self.verificar_texto("Teatro Amazonas", "#firstHeading")
        self.verificar_texto_do_link("Festival Amazonas de Ópera")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/portuguese_test_1.py">examples/translations/portuguese_test_1.py</a> for the Portuguese test.)

<a id="sb_sf_18"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 18. BaseCase with Russian translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Russian. Here's an example of that:

```python
from seleniumbase.translate.russian import ТестНаСелен
ТестНаСелен.main(__name__, __file__)


class МойТестовыйКласс(ТестНаСелен):
    def test_пример_1(self):
        self.открыть("https://ru.wikipedia.org/wiki/")
        self.подтвердить_элемент('[title="Русский язык"]')
        self.подтвердить_текст("Википедия", "h2.main-wikimedia-header")
        self.введите("#searchInput", "МГУ")
        self.нажмите("#searchButton")
        self.подтвердить_текст("университет", "#firstHeading")
        self.подтвердить_элемент('img[alt*="Главное здание МГУ"]')
        self.введите("#searchInput", "приключения Шурика")
        self.нажмите("#searchButton")
        self.подтвердить_текст("Операция «Ы» и другие приключения Шурика")
        self.подтвердить_элемент('img[alt="Постер фильма"]')
        self.назад()
        self.подтвердить_URL_содержит("университет")
        self.вперед()
        self.подтвердить_URL_содержит("Шурика")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/russian_test_1.py">examples/translations/russian_test_1.py</a> for the Russian test.)

<a id="sb_sf_19"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 19. BaseCase with Spanish translations</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Spanish. Here's an example of that:

```python
from seleniumbase.translate.spanish import CasoDePrueba
CasoDePrueba.main(__name__, __file__)


class MiClaseDePrueba(CasoDePrueba):
    def test_ejemplo_1(self):
        self.abrir("https://es.wikipedia.org/wiki/")
        self.verificar_texto("Wikipedia")
        self.verificar_elemento('[title*="la página principal"]')
        self.escriba("#searchInput", "Parc d'Atraccions Tibidabo")
        self.haga_clic("#searchButton")
        self.verificar_texto("Tibidabo", "#firstHeading")
        self.verificar_elemento('img[alt*="Tibidabo"]')
        self.escriba("#searchInput", "Palma de Mallorca")
        self.haga_clic("#searchButton")
        self.verificar_texto("Palma de Mallorca", "#firstHeading")
        self.verificar_elemento('img[alt*="Palma"]')
        self.volver()
        self.verificar_url_contiene("Tibidabo")
        self.adelante()
        self.verificar_url_contiene("Mallorca")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/spanish_test_1.py">examples/translations/spanish_test_1.py</a> for the Spanish test.)

<a id="sb_sf_20"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 20. Gherkin syntax with "behave" BDD runner</h3>

With [Behave's BDD Gherkin format](https://behave.readthedocs.io/en/stable/gherkin.html), you can use natural language to write tests that work with SeleniumBase methods. Behave tests are run by calling ``behave`` on the command-line. This requires some special files in a specific directory structure. Here's an example of that structure:

```bash
features/
├── __init__.py
├── behave.ini
├── environment.py
├── feature_file.feature
└── steps/
    ├── __init__.py
    ├── imported.py
    └── step_file.py
```

A ``*.feature`` file might look like this:

```gherkin
Feature: SeleniumBase scenarios for the RealWorld App

  Scenario: Verify RealWorld App (log in / sign out)
    Given Open "seleniumbase.io/realworld/login"
    And Clear Session Storage
    When Type "demo_user" into "#username"
    And Type "secret_pass" into "#password"
    And Do MFA "GAXG2MTEOR3DMMDG" into "#totpcode"
    Then Assert exact text "Welcome!" in "h1"
    And Highlight "img#image1"
    And Click 'a:contains("This Page")'
    And Save screenshot to logs
    When Click link "Sign out"
    Then Assert element 'a:contains("Sign in")'
    And Assert text "You have been signed out!"
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd/features/realworld.feature">examples/behave_bdd/features/realworld.feature</a>)

You'll need the ``environment.py`` file for tests to work. Here it is:

```python
from seleniumbase import BaseCase
from seleniumbase.behave import behave_sb
behave_sb.set_base_class(BaseCase)  # Accepts a BaseCase subclass
from seleniumbase.behave.behave_sb import before_all  # noqa
from seleniumbase.behave.behave_sb import before_feature  # noqa
from seleniumbase.behave.behave_sb import before_scenario  # noqa
from seleniumbase.behave.behave_sb import before_step  # noqa
from seleniumbase.behave.behave_sb import after_step  # noqa
from seleniumbase.behave.behave_sb import after_scenario  # noqa
from seleniumbase.behave.behave_sb import after_feature  # noqa
from seleniumbase.behave.behave_sb import after_all  # noqa
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd/features/environment.py">examples/behave_bdd/features/environment.py</a>)

Inside that file, you can use ``BaseCase`` (or a subclass) for the inherited class.

For your ``behave`` tests to have access to SeleniumBase Behave steps, you can create an ``imported.py`` file with the following line:

```python
from seleniumbase.behave import steps  # noqa
```

That will allow you to use lines like this in your ``*.feature`` files:

```gherkin
Feature: SeleniumBase scenarios for the RealWorld App

  Scenario: Verify RealWorld App (log in / sign out)
    Given Open "seleniumbase.io/realworld/login"
    And Clear Session Storage
    When Type "demo_user" into "#username"
    And Type "secret_pass" into "#password"
    And Do MFA "GAXG2MTEOR3DMMDG" into "#totpcode"
    Then Assert exact text "Welcome!" in "h1"
    And Highlight "img#image1"
    And Click 'a:contains("This Page")'
    And Save screenshot to logs
```

You can also create your own step files (Eg. ``step_file.py``):

```python
from behave import step

@step("Open the Swag Labs Login Page")
def go_to_swag_labs(context):
    sb = context.sb
    sb.open("https://www.saucedemo.com")
    sb.clear_local_storage()

@step("Login to Swag Labs with {user}")
def login_to_swag_labs(context, user):
    sb = context.sb
    sb.type("#user-name", user)
    sb.type("#password", "secret_sauce\n")
```

(For more information, see the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd/ReadMe.md">SeleniumBase Behave BDD ReadMe</a>.)

<a id="sb_sf_21"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 21. SeleniumBase SB (Python context manager)</h3>

This format provides a pure Python way of using SeleniumBase without a test runner. Options can be passed via method instantiation or from the command-line. When setting the <code>test</code> option to <code>True</code> (or calling <code>python --test</code>), then standard test logging will occur, such as screenshots and reports for failing tests. All the usual SeleniumBase options are available, such as customizing the browser settings, etc. Here are some examples:

```python
from seleniumbase import SB

with SB() as sb:  # By default, browser="chrome" if not set.
    sb.open("https://seleniumbase.github.io/realworld/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
    sb.assert_text("Welcome!", "h1")
    sb.highlight("img#image1")  # A fancier assert_element() call
    sb.click('a:contains("This Page")')  # Use :contains() on any tag
    sb.click_link("Sign out")  # Link must be "a" tag. Not "button".
    sb.assert_element('a:contains("Sign in")')
    sb.assert_exact_text("You have been signed out!", "#top_message")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_sb.py">examples/raw_sb.py</a> for the test.)

Here's another example, which uses <code>test</code> mode:

```python
from seleniumbase import SB

with SB(test=True) as sb:
    sb.open("https://google.com/ncr")
    sb.type('[name="q"]', "SeleniumBase on GitHub\n")
    sb.click('a[href*="github.com/seleniumbase"]')
    sb.highlight("div.Layout-main")
    sb.highlight("div.Layout-sidebar")
    sb.sleep(0.5)

with SB(test=True, rtf=True, demo=True) as sb:
    sb.open("seleniumbase.github.io/demo_page")
    sb.type("#myTextInput", "This is Automated")
    sb.assert_text("This is Automated", "#myTextInput")
    sb.assert_text("This Text is Green", "#pText")
    sb.click('button:contains("Click Me")')
    sb.assert_text("This Text is Purple", "#pText")
    sb.click("#checkBox1")
    sb.assert_element_not_visible("div#drop2 img#logo")
    sb.drag_and_drop("img#logo", "div#drop2")
    sb.assert_element("div#drop2 img#logo")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_test_scripts.py">examples/raw_test_scripts.py</a> for the test.)

<a id="sb_sf_22"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 22. The driver manager (via context manager)</h3>

This pure Python format gives you a raw <code>webdriver</code> instance in a <code>with</code> block. The SeleniumBase Driver Manager will automatically make sure that your driver is compatible with your browser version. It gives you full access to customize driver options via method args or via the command-line. The driver will automatically call <code>quit()</code> after the code leaves the <code>with</code> block. Here are some examples:

```python
"""This script can be run with pure "python". (pytest not needed)."""
from seleniumbase import js_utils
from seleniumbase import page_actions
from seleniumbase import DriverContext

# Driver Context Manager - (By default, browser="chrome". Lots of options)
with DriverContext() as driver:
    driver.get("https://seleniumbase.github.io/")
    js_utils.highlight_with_js(driver, 'img[alt="SeleniumBase"]', loops=6)

with DriverContext(browser="chrome", incognito=True) as driver:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element(driver, "4", by="id").click()
    page_actions.wait_for_element(driver, "2", by="id").click()
    page_actions.wait_for_text(driver, "42", "output", by="id")
    js_utils.highlight_with_js(driver, "#output", loops=6)

with DriverContext() as driver:
    driver.get("https://seleniumbase.github.io/demo_page")
    js_utils.highlight_with_js(driver, "h2", loops=5)
    by_css = "css selector"
    driver.find_element(by_css, "#myTextInput").send_keys("Automation")
    driver.find_element(by_css, "#checkBox1").click()
    js_utils.highlight_with_js(driver, "img", loops=5)
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_driver_context.py">examples/raw_driver_context.py</a> for an example.)

<a id="sb_sf_23"></a>
<h3><img src="https://seleniumbase.github.io/img/logo3b.png" title="SeleniumBase" width="32" /> 23. The driver manager (via direct import)</h3>

Another way of running Selenium tests with pure ``python`` (as opposed to using ``pytest`` or ``nosetests``) is by using this format, which bypasses [BaseCase](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py) methods while still giving you a flexible driver with a manager. SeleniumBase includes helper files such as [page_actions.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/page_actions.py), which may help you get around some of the limitations of bypassing ``BaseCase``. Here's an example:

```python
"""This script can be run with pure "python". (pytest not needed)."""
from seleniumbase import Driver
from seleniumbase import js_utils
from seleniumbase import page_actions

# Example with options. (Also accepts command-line options.)
driver = Driver(browser="chrome", headless=False)
try:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element(driver, "4", by="id").click()
    page_actions.wait_for_element(driver, "2", by="id").click()
    page_actions.wait_for_text(driver, "42", "output", by="id")
    js_utils.highlight_with_js(driver, "#output", loops=6)
finally:
    driver.quit()

# Example 2 using default args or command-line options
driver = Driver()
try:
    driver.get("https://seleniumbase.github.io/demo_page")
    js_utils.highlight_with_js(driver, "h2", loops=5)
    by_css = "css selector"
    driver.find_element(by_css, "#myTextInput").send_keys("Automation")
    driver.find_element(by_css, "#checkBox1").click()
    js_utils.highlight_with_js(driver, "img", loops=5)
finally:
    driver.quit()
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_browser_launcher.py">examples/raw_browser_launcher.py</a>)

The above format can be used as a drop-in replacement for virtually every Python/selenium framework, as it uses the raw ``driver`` instance for handling commands. The ``Driver()`` method simplifies the work of managing drivers with optimal settings, and it can be configured via multiple method args. The Driver also accepts command-line options (such as ``python --headless``) so that you don't need to modify your tests directly to use different settings. These command-line options only take effect if the associated method args remain unset (or set to ``None``) for the specified options.

--------

<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/sb_logo_10.png" title="SeleniumBase" width="280" /></a></h3>
