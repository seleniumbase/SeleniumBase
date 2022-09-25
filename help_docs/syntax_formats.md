<a id="syntax_formats"></a>

## [<img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) The 20 Syntax Formats

<b>SeleniumBase</b> supports 20 different syntax formats (<i>design patterns</i>) for structuring tests. (<i>The first 6 are the most common.</i>)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 1. <code>BaseCase</code> direct inheritance</h3>

This format is used by most of the examples in the <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples">SeleniumBase examples folder</a>. It's a great starting point for anyone learning SeleniumBase, and it follows good object-oriented programming principles. In this format, <code>BaseCase</code> is imported at the top of a Python file, followed by a Python class inheriting <code>BaseCase</code>. Then, any test method defined in that class automatically gains access to SeleniumBase methods, including the <code>setUp()</code> and <code>tearDown()</code> methods that are automatically called to spin up and spin down web browsers at the beginning and end of test methods. Here's an example of that:

```python
from seleniumbase import BaseCase

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 2. <code>BaseCase</code> subclass inheritance</h3>

There are situations where you may want to customize the <code>setUp</code> and <code>tearDown</code> of your tests. Maybe you want to have all your tests login to a specific web site first, or maybe you want to have your tests report results through an API call depending on whether a test passed or failed. <b>This can be done by creating a subclass of <code>BaseCase</code> and then carefully creating custom <code>setUp()</code> and <code>tearDown()</code> methods that don't overwrite the critical functionality of the default SeleniumBase <code>setUp()</code> and <code>tearDown()</code> methods.</b> Afterwards, your test classes will inherit the subclass of <code>BaseCase</code> with the added functionality, rather than directly inheriting <code>BaseCase</code> itself. Here's an example of that:

```python
from seleniumbase import BaseCase

class BaseTestCase(BaseCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        # <<< Run custom setUp() code for tests AFTER the super().setUp() >>>

    def tearDown(self):
        self.save_teardown_screenshot()  # If test fails, or if "--screenshot"
        if self.has_exception():
            # <<< Run custom code if the test failed. >>>
            pass
        else:
            # <<< Run custom code if the test passed. >>>
            pass
        # (Wrap unreliable tearDown() code in a try/except block.)
        # <<< Run custom tearDown() code BEFORE the super().tearDown() >>>
        super(BaseTestCase, self).tearDown()

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 3. The <code>sb</code> pytest fixture (no class)</h3>

The pytest framework comes with a unique system called fixtures, which replaces import statements at the top of Python files by importing libraries directly into test definitions. More than just being an import, a pytest fixture can also automatically call predefined <code>setUp()</code> and <code>tearDown()</code> methods at the beginning and end of test methods. To work, <code>sb</code> is added as an argument to each test method definition that needs SeleniumBase functionality. This means you no longer need import statements in your Python files to use SeleniumBase. <b>If using other pytest fixtures in your tests, you may need to use the SeleniumBase fixture (instead of <code>BaseCase</code> class inheritance) for compatibility reasons.</b> Here's an example of the <code>sb</code> fixture in a test that does not use Python classes:

```python
def test_sb_fixture_with_no_class(sb):
    sb.open("https://google.com/ncr")
    sb.type('input[title="Search"]', 'SeleniumBase\n')
    sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
    sb.click('a[title="seleniumbase"]')
```

(See the top of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_sb_fixture.py">examples/test_sb_fixture.py</a> for the test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 4. The <code>sb</code> pytest fixture (in class)</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 5. The classic Page Object Model with <code>BaseCase</code> inheritance</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 6. The classic Page Object Model with the <code>sb</code> pytest fixture</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 7. Using the <code>request</code> fixture to get the <code>sb</code> fixture (no class)</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 8. Using the <code>request</code> fixture to get the <code>sb</code> fixture (in class)</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 9. Overriding the SeleniumBase browser launcher </h3>

When you want to use SeleniumBase methods, but you want total freedom to control how you spin up your web browsers, this is the format you want. Although SeleniumBase gives you plenty of command-line options to change how your browsers are launched, this format gives you even more control. Here's an example of that:

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
            options.add_argument("--headless")
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

The above format lets you use [selenium-wire](https://github.com/wkeeling/selenium-wire) to intercept & inspect requests and responses during SeleniumBase tests. Here's how the ``selenium-wire`` integration may look:

```python
from seleniumbase import BaseCase
from seleniumwire import webdriver  # the selenium-wire webdriver


class WireTestCase(BaseCase):
    def get_new_driver(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        return webdriver.Chrome(options=options)

    def test_simple(self):
        self.open("https://seleniumbase.io/demo_page")
        for request in self.driver.requests:
            print(request.url)
```

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 10. Using the SeleniumBase browser launcher without BaseCase </h3>

One way of running Selenium tests with pure ``python`` (as opposed to using ``pytest`` or ``nosetests``) is by using this format, which bypasses [BaseCase](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py) methods while still giving you ``browser_launcher`` with its powerful webdriver management software. SeleniumBase includes helper files such as [page_actions.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/page_actions.py), which may help you get around some of the limitations of bypassing ``BaseCase``. Here's an example:

```python
from seleniumbase import get_driver
from seleniumbase import js_utils
from seleniumbase import page_actions

driver = get_driver("chrome", headless=False)
try:
    driver.get("https://seleniumbase.io/apps/calculator")
    page_actions.wait_for_element_visible(driver, "4", "id").click()
    page_actions.wait_for_element_visible(driver, "2", "id").click()
    page_actions.wait_for_text_visible(driver, "42", "output", "id")
    js_utils.highlight_with_js(driver, "#output", 6, "")
finally:
    driver.quit()
```

(From <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_browser_launcher.py">examples/raw_browser_launcher.py</a>)

The above format can be used as a drop-in replacement for virtually every Python/selenium framework, as it uses the raw ``driver`` for handling commands. The ``get_driver()`` method simplifies the work of managing drivers and spinning them up with optimal settings. Note that now you'll need to manage the spin-up and spin-down of browsers in tests, which was done automatically in tests that inherit ``BaseCase`` (or ones that use the ``sb`` pytest fixture). You'll also need to use extra code (as shown above) to make sure you don't leave any browsers hanging after your tests complete.

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 11. SeleniumBase in Chinese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Chinese. Here's an example of that:

```python
from seleniumbase.translate.chinese import 硒测试用例

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 12. SeleniumBase in Dutch</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Dutch. Here's an example of that:

```python
from seleniumbase.translate.dutch import Testgeval

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
        self.controleren_ware("Stroopwafel" in self.huidige_url_ophalen())
        self.vooruit()
        self.controleren_ware("Rijksmuseum" in self.huidige_url_ophalen())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/dutch_test_1.py">examples/translations/dutch_test_1.py</a> for the Dutch test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 13. SeleniumBase in French</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into French. Here's an example of that:

```python
from seleniumbase.translate.french import CasDeBase

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
        self.vérifier_vrai("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_vrai("Jardin" in self.obtenir_url_actuelle())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/french_test_1.py">examples/translations/french_test_1.py</a> for the French test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 14. SeleniumBase in Italian</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Italian. Here's an example of that:

```python
from seleniumbase.translate.italian import CasoDiProva

class MiaClasseDiTest(CasoDiProva):
    def test_esempio_1(self):
        self.apri("https://it.wikipedia.org/wiki/")
        self.verificare_testo("Wikipedia")
        self.verificare_elemento('[title="Lingua italiana"]')
        self.digitare("#searchInput", "Pizza")
        self.fare_clic("#searchButton")
        self.verificare_testo("Pizza", "#firstHeading")
        self.verificare_elemento('img[alt*="pizza"]')
        self.digitare("#searchInput", "Colosseo")
        self.fare_clic("#searchButton")
        self.verificare_testo("Colosseo", "#firstHeading")
        self.verificare_elemento('img[alt*="Colosse"]')
        self.indietro()
        self.verificare_vero("Pizza" in self.ottenere_url_corrente())
        self.avanti()
        self.verificare_vero("Colosseo" in self.ottenere_url_corrente())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/italian_test_1.py">examples/translations/italian_test_1.py</a> for the Italian test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 15. SeleniumBase in Japanese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Japanese. Here's an example of that:

```python
from seleniumbase.translate.japanese import セレニウムテストケース

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 16. SeleniumBase in Korean</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Korean. Here's an example of that:

```python
from seleniumbase.translate.korean import 셀레늄_테스트_케이스

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 17. SeleniumBase in Portuguese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Portuguese. Here's an example of that:

```python
from seleniumbase.translate.portuguese import CasoDeTeste

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
        self.verificar_verdade("João" in self.obter_url_atual())
        self.atualizar_a_página()
        self.digitar("#searchform input", "Teatro Amazonas")
        self.clique("#searchform button")
        self.verificar_texto("Teatro Amazonas", "#firstHeading")
        self.verificar_texto_do_link("Festival Amazonas de Ópera")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/portuguese_test_1.py">examples/translations/portuguese_test_1.py</a> for the Portuguese test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 18. SeleniumBase in Russian</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Russian. Here's an example of that:

```python
from seleniumbase.translate.russian import ТестНаСелен

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
        self.подтвердить_правду("университет" in self.получить_текущий_URL())
        self.вперед()
        self.подтвердить_правду("Шурика" in self.получить_текущий_URL())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/russian_test_1.py">examples/translations/russian_test_1.py</a> for the Russian test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 19. SeleniumBase in Spanish</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Spanish. Here's an example of that:

```python
from seleniumbase.translate.spanish import CasoDePrueba

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
        self.verificar_verdad("Tibidabo" in self.obtener_url_actual())
        self.adelante()
        self.verificar_verdad("Mallorca" in self.obtener_url_actual())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/spanish_test_1.py">examples/translations/spanish_test_1.py</a> for the Spanish test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 20. Behave-BDD Gherkin tests that use SeleniumBase </h3>

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

You can also create your own step files (eg. ``step_file.py``):

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

--------

<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/img/sb_logo_10.png" title="SeleniumBase" width="280" /></a></h3>
