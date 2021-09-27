<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/mac_sb_logo_3.png" title="SeleniumBase" width="300" /></a></h3>

<a id="language_tests"></a>
<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Language Tests (Python 3+)</h3>

<b>SeleniumBase</b> supports the following 10 languages: <i>English</i>, <i>Chinese</i>, <i>Dutch</i>, <i>French</i>, <i>Italian</i>, <i>Japanese</i>, <i>Korean</i>, <i>Portuguese</i>, <i>Russian</i>, and <i>Spanish</i>.

Examples can be found in [<a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/translations">SeleniumBase/examples/translations</a>].

Multi-language tests are run with **pytest** like any other test. Test methods have a one-to-one mapping to the other supported languages. Here's an example of a translated test:

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
```

<a id="translation_api"></a>
<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Translation API</h2>

You can use SeleniumBase to selectively translate the method names of any test from one language to another with the console scripts interface. Additionally, the ``import`` line at the top of the Python file will change to import the new ``BaseCase``. Example: ``BaseCase`` becomes ``CasoDeTeste`` when a test is translated into Portuguese.

```bash
seleniumbase translate
```

```bash
* Usage:
seleniumbase translate [SB_FILE.py] [LANGUAGE] [ACTION]

* Languages:
``--en`` / ``--English``  |  ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``    |  ``--fr`` / ``--French``
``--it`` / ``--Italian``  |  ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``   |  ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``  |  ``--es`` / ``--Spanish``

* Actions:
``-p`` / ``--print``  (Print translation output to the screen)
``-o`` / ``--overwrite``  (Overwrite the file being translated)
``-c`` / ``--copy``  (Copy the translation to a new ``.py`` file)

* Options:
``-n``  (include line Numbers when using the Print action)

* Examples:
Translate test_1.py into Chinese and only print the output:
>>> seleniumbase translate test_1.py --zh  -p
Translate test_2.py into Portuguese and overwrite the file:
>>> seleniumbase translate test_2.py --pt  -o
Translate test_3.py into Dutch and make a copy of the file:
>>> seleniumbase translate test_3.py --nl  -c

* Output:
Translates a SeleniumBase Python file into the language
specified. Method calls and ``import`` lines get swapped.
Both a language and an action must be specified.
The ``-p`` action can be paired with one other action.
When running with ``-c`` (or ``--copy``) the new file name
will be the original name appended with an underscore
plus the 2-letter language code of the new language.
(Example: Translating ``test_1.py`` into Japanese with
``-c`` will create a new file called ``test_1_ja.py``.)
```

--------

<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/super_logo_m.png" title="SeleniumBase" width="280" /></a></h3>
