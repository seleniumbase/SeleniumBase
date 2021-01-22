<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/mac_sb_logo_3.png" title="SeleniumBase" width="360" /></a></h3>

<a id="syntax_formats"></a>
<h2><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> The 15 unique syntax formats</h2>

<p>(<b><a href="https://www.youtube.com/watch?v=Sjzq9kU5kOw">Watch this tutorial on YouTube</a></b>)</p>

[<img src="http://img.youtube.com/vi/HOooW_0o468/0.jpg" title="The 15 unique syntax formats" width="255">](https://www.youtube.com/watch?v=HOooW_0o468)

--------

<b>SeleniumBase</b> supports 15 different syntax formats for structuring tests. (<i>The first 4 are the most common.</i>)

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
        self.click_link_text("SeleniumBase Demo Page")
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
        self.save_teardown_screenshot()
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
class Test_SB_Fixture():
    def test_sb_fixture_inside_class(self, sb):
        sb.open("https://google.com/ncr")
        sb.type('input[title="Search"]', 'SeleniumBase\n')
        sb.click('a[href*="github.com/seleniumbase/SeleniumBase"]')
        sb.click('a[title="examples"]')
```

(See the bottom of <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_sb_fixture.py">examples/test_sb_fixture.py</a> for the test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 5. Using the <code>request</code> fixture to get the <code>sb</code> fixture (no class)</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 6. Using the <code>request</code> fixture to get the <code>sb</code> fixture (in class)</h3>

The pytest <code>request</code> fixture can also be used to get the <code>sb</code> fixture from inside a Python class. Here's an example of that:

```python
class Test_Request_Fixture():
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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 7. SeleniumBase in Chinese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Chinese. Here's an example of that:

```python
from seleniumbase.translate.chinese import 硒测试用例

class 我的测试类(硒测试用例):
    def test_例子1(self):
        self.开启网址("https://xkcd.in/comic?lg=cn&id=353")
        self.断言标题("Python - XKCD中文站")
        self.断言元素("#content div.comic-body")
        self.断言文本("上漫画")
        self.单击("div.nextLink")
        self.断言文本("母亲的功绩", "#content h1")
        self.单击链接文本("下一篇")
        self.断言文本("敲打", "#content h1")
        self.断言文本("有时，最有趣的事也会显得无聊")
        self.回去()
        self.单击链接文本("兰德尔·门罗")
        self.断言文本("兰德尔·门罗", "#firstHeading")
        self.输入文本("#searchInput", "程式设计")
        self.单击("#searchButton")
        self.断言文本("程序设计", "#firstHeading")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/chinese_test_1.py">examples/translations/chinese_test_1.py</a> for the Chinese test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 8. SeleniumBase in Dutch</h3>

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
        self.controleren_element('img[alt="Stroopwafels"]')
        self.typ("#searchInput", "Rijksmuseum Amsterdam")
        self.klik("#searchButton")
        self.controleren_tekst("Rijksmuseum", "#firstHeading")
        self.controleren_element('img[alt="Het Rijksmuseum"]')
        self.terug()
        self.controleren_ware("Stroopwafel" in self.huidige_url_ophalen())
        self.vooruit()
        self.controleren_ware("Rijksmuseum" in self.huidige_url_ophalen())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/dutch_test_1.py">examples/translations/dutch_test_1.py</a> for the Dutch test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 9. SeleniumBase in French</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into French. Here's an example of that:

```python
from seleniumbase.translate.french import CasDeBase

class MaClasseDeTest(CasDeBase):
    def test_exemple_1(self):
        self.ouvrir("https://fr.wikipedia.org/wiki/")
        self.vérifier_texte("Wikipédia")
        self.vérifier_élément('[alt="Wikipédia"]')
        self.taper("#searchInput", "Crème brûlée")
        self.cliquer("#searchButton")
        self.vérifier_texte("Crème brûlée", "#firstHeading")
        self.vérifier_élément('img[alt*="Crème brûlée"]')
        self.taper("#searchInput", "Jardin des Tuileries")
        self.cliquer("#searchButton")
        self.vérifier_texte("Jardin des Tuileries", "#firstHeading")
        self.vérifier_élément('img[alt*="Jardin des Tuileries"]')
        self.retour()
        self.vérifier_vrai("brûlée" in self.obtenir_url_actuelle())
        self.en_avant()
        self.vérifier_vrai("Jardin" in self.obtenir_url_actuelle())
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/french_test_1.py">examples/translations/french_test_1.py</a> for the French test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 10. SeleniumBase in Italian</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 11. SeleniumBase in Japanese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Japanese. Here's an example of that:

```python
from seleniumbase.translate.japanese import セレニウムテストケース

class 私のテストクラス(セレニウムテストケース):
    def test_例1(self):
        self.を開く("https://ja.wikipedia.org/wiki/")
        self.テキストを確認する("ウィキペディア")
        self.要素を確認する('[title="メインページに移動する"]')
        self.入力("#searchInput", "アニメ")
        self.クリックして("#searchButton")
        self.テキストを確認する("アニメ", "#firstHeading")
        self.入力("#searchInput", "寿司")
        self.クリックして("#searchButton")
        self.テキストを確認する("寿司", "#firstHeading")
        self.要素を確認する('img[alt="握り寿司"]')
        self.入力("#searchInput", "レゴランド・ジャパン")
        self.クリックして("#searchButton")
        self.要素を確認する('img[alt="Legoland japan.jpg"]')
        self.リンクテキストを確認する("名古屋城")
        self.リンクテキストをクリックします("テーマパーク")
        self.テキストを確認する("テーマパーク", "#firstHeading")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/japanese_test_1.py">examples/translations/japanese_test_1.py</a> for the Japanese test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 12. SeleniumBase in Korean</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Korean. Here's an example of that:

```python
from seleniumbase.translate.korean import 셀레늄_테스트_케이스

class 테스트_클래스(셀레늄_테스트_케이스):
    def test_실시예_1(self):
        self.열기("https://ko.wikipedia.org/wiki/")
        self.텍스트_확인("위키백과")
        self.요소_확인('[title="위키백과:소개"]')
        self.입력("#searchInput", "김치")
        self.클릭("#searchButton")
        self.텍스트_확인("김치", "#firstHeading")
        self.요소_확인('img[alt="Various kimchi.jpg"]')
        self.링크_텍스트_확인("한국 요리")
        self.입력("#searchInput", "비빔밥")
        self.클릭("#searchButton")
        self.텍스트_확인("비빔밥", "#firstHeading")
        self.요소_확인('img[alt="Dolsot-bibimbap.jpg"]')
        self.링크_텍스트를_클릭합니다("돌솥비빔밥")
        self.텍스트_확인("돌솥비빔밥", "#firstHeading")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/korean_test_1.py">examples/translations/korean_test_1.py</a> for the Korean test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 13. SeleniumBase in Portuguese</h3>

This format is similar to the English version with <code>BaseCase</code> inheritance, but there's a different import statement, and method names have been translated into Portuguese. Here's an example of that:

```python
from seleniumbase.translate.portuguese import CasoDeTeste

class MinhaClasseDeTeste(CasoDeTeste):
    def test_exemplo_1(self):
        self.abrir("https://pt.wikipedia.org/wiki/")
        self.verificar_texto("Wikipédia")
        self.verificar_elemento('[title="Língua portuguesa"]')
        self.tipo("#searchInput", "João Pessoa")
        self.clique("#searchButton")
        self.verificar_texto("João Pessoa", "#firstHeading")
        self.verificar_elemento('img[alt*="João Pessoa"]')
        self.tipo("#searchInput", "Florianópolis")
        self.clique("#searchButton")
        self.verificar_texto("Florianópolis", "h1#firstHeading")
        self.verificar_elemento('img[alt*="Avenida Beira Mar"]')
        self.voltar()
        self.verificar_verdade("João" in self.obter_url_atual())
        self.tipo("#searchInput", "Teatro Amazonas")
        self.clique("#searchButton")
        self.verificar_texto("Teatro Amazonas", "#firstHeading")
        self.verificar_texto_do_link("Festival Amazonas de Ópera")
```

(See <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/portuguese_test_1.py">examples/translations/portuguese_test_1.py</a> for the Portuguese test.)

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 14. SeleniumBase in Russian</h3>

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

<h3><img src="https://seleniumbase.io/img/green_logo.png" title="SeleniumBase" width="32" /> 15. SeleniumBase in Spanish</h3>

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

--------

<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/img/sb_logo_10.png" title="SeleniumBase" width="280" /></a></h3>
