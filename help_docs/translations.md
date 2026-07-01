<!-- SeleniumBase Docs -->

<a id="language_tests"></a>

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> 🌏 Translated Tests 🈺</h2>

<b>SeleniumBase</b> supports the following 10 languages: <i>English</i>, <i>Chinese</i>, <i>Dutch</i>, <i>French</i>, <i>Italian</i>, <i>Japanese</i>, <i>Korean</i>, <i>Portuguese</i>, <i>Russian</i>, and <i>Spanish</i>. (Examples can be found in <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/translations">SeleniumBase/examples/translations</a>)

Multi-language tests run with **pytest** like other tests. Test methods have a one-to-one mapping to supported languages. Here's an example of a translated test:

```python
# Chinese Translation
from seleniumbase.translate.chinese import 硒测试用例

class 我的测试类(硒测试用例):
    def test_例子1(self):
        self.开启("https://zh.wikipedia.org/wiki/")
        self.断言标题("维基百科，自由的百科全书")
        self.断言元素('a[title="Wikipedia:关于"]')
        self.如果可见请单击('button[aria-label="关闭"]')
        self.如果可见请单击('button[aria-label="關閉"]')
        self.断言元素('span:contains("创建账号")')
        self.断言元素('span:contains("登录")')
        self.输入文本('input[name="search"]', "舞龍")
        self.单击('button:contains("搜索")')
        self.断言文本("舞龍", "#firstHeading")
        self.断言元素('img[src*="Chinese_draak.jpg"]')
```

Here's another example:

```python
# Japanese Translation
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
        self.要素を確認する('img[src*="Various_sushi"]')
```

<a id="translation_api"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Translation API 🈺</h2>

You can use SeleniumBase to selectively translate the method names of any test from one language to another with the console scripts interface. Additionally, the `import` line at the top of the Python file will change to import the new `BaseCase`. Example: `BaseCase` becomes `CasoDeTeste` when a test is translated into Portuguese.

```zsh
seleniumbase translate
```

```zsh
* Usage:
seleniumbase translate [SB_FILE.py] [LANGUAGE] [ACTION]

* Languages:
`--en` / `--English`  |  `--zh` / `--Chinese`
`--nl` / `--Dutch`    |  `--fr` / `--French`
`--it` / `--Italian`  |  `--ja` / `--Japanese`
`--ko` / `--Korean`   |  `--pt` / `--Portuguese`
`--ru` / `--Russian`  |  `--es` / `--Spanish`

* Actions:
`-p` / `--print`  (Print translation output to the screen)
`-o` / `--overwrite`  (Overwrite the file being translated)
`-c` / `--copy`  (Copy the translation to a new `.py` file)

* Options:
`-n`  (include line Numbers when using the Print action)

* Examples:
Translate test_1.py into Chinese and only print the output:
>>> seleniumbase translate test_1.py --zh  -p
Translate test_2.py into Portuguese and overwrite the file:
>>> seleniumbase translate test_2.py --pt  -o
Translate test_3.py into Dutch and make a copy of the file:
>>> seleniumbase translate test_3.py --nl  -c

* Output:
Translates a SeleniumBase Python file into the language
specified. Method calls and `import` lines get swapped.
Both a language and an action must be specified.
The `-p` action can be paired with one other action.
When running with `-c` (or `--copy`) the new file name
will be the original name appended with an underscore
plus the 2-letter language code of the new language.
(Example: Translating `test_1.py` into Japanese with
`-c` will create a new file called `test_1_ja.py`.)
```

--------

<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/cdn/img/super_logo_m.png" title="SeleniumBase" width="280" /></a></h3>
