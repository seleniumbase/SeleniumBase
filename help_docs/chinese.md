<meta property="og:site_name" content="SeleniumBase | Docs">
<meta property="og:title" content="SeleniumBase | Reliable Test Automation" />
<meta property="og:description" content="Simple browser automation and testing with Python." />
<meta property="og:image" content="https://seleniumbase.io/img/sb_logo_7.png" />
<link rel="icon" href="https://seleniumbase.io/img/logo3a.png" />
<section align="center"><div align="center">
<h2>✅ 可靠的测试自动化</h2>
</div></section>
<p align="center"><a href="https://github.com/seleniumbase/SeleniumBase/">
<img src="https://seleniumbase.io/img/sb_logo_7.png" alt="SeleniumBase" width="260" />
</a></p>
<p align="center"><div align="center"><b>测试框架 </b><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/✅%20💛%20查看代码-在GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a></div></p>
<section align="center"><div align="center"><h3>中文文件 <=> <a href="https://seleniumbase.io/">English Docs</h3></div></section>

<p align="center">
<a href="https://github.com/seleniumbase/SeleniumBase/releases">
<img src="https://img.shields.io/github/v/release/seleniumbase/SeleniumBase.svg?color=2277EE" alt="Latest Release on GitHub" /></a> <a href="https://pypi.python.org/pypi/seleniumbase">
<img src="https://img.shields.io/pypi/v/seleniumbase.svg?color=22AAEE" alt="Latest Release on PyPI" /></a> <a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20📖-11BBDD.svg" alt="SeleniumBase.io Docs" /></a> <a href="https://seleniumbase.io/help_docs/chinese/">
<img src="https://img.shields.io/badge/文件-%20中文-11BBDD.svg" alt="SeleniumBase.io Docs" /></a> <a href="https://travis-ci.org/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/travis/seleniumbase/SeleniumBase/master.svg" alt="SeleniumBase on TravisCI" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/actions">
<img src="https://github.com/seleniumbase/SeleniumBase/workflows/CI%20build/badge.svg" alt="SeleniumBase GitHub Actions" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase">
<img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" alt="SeleniumBase" /></a>
</p>

<p align="center">
<b>UI自动化测试需要的一切这里都有.</b>
</p>

<p align="center">
<a href="#python_installation">🚀 立即开始</a> |
<a href="https://seleniumbase.io/help_docs/customizing_test_runs/">🧙‍♂️ 命令行选项</a> |
<a href="https://seleniumbase.io/help_docs/features_list/">🏰 功能列表</a> |
<a href="https://seleniumbase.io/examples/ReadMe/">👨‍🏫 学习示例</a> |
<a href="https://seleniumbase.io/help_docs/mobile_testing/">📱 移动测试</a> |
<a href="https://seleniumbase.io/examples/example_logs/ReadMe/">📊 测试报告</a>
<br />
<a href="https://seleniumbase.io/help_docs/method_summary/">📖 API语法</a> |
<a href="https://seleniumbase.io/examples/tour_examples/ReadMe/">🗺️ 创建旅游</a> |
<a href="https://seleniumbase.io/help_docs/translations/">🌎 语言翻译</a> |
<a href="https://seleniumbase.io/seleniumbase/utilities/selenium_ide/ReadMe/">⏺️ 录音机工具</a> |
<a href="https://seleniumbase.io/examples/master_qa/ReadMe/">🛂 MasterQA</a> |
<a href="https://seleniumbase.io/integrations/github/workflows/ReadMe/">🤖 持续集成</a>
</p>

<p align="center">
<div align="center"><b>Selenium 和 pytest 组合使用.</b></div>
</p>
<p align="center"><div align="center"><img src="https://seleniumbase.io/cdn/gif/swag_demo_2.gif" alt="SeleniumBase" title="SeleniumBase" /></div></p>

<a id="python_installation"></a>
<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 立即开始:</h2>

* 需要 **[Python](https://www.python.org/downloads/)** 和 **[Git](https://git-scm.com/)**
* [<img src="https://img.shields.io/pypi/pyversions/seleniumbase.svg?color=22AAEE" alt="Python:2.7|3.5|3.6|3.7|3.8" />](https://www.python.org/downloads/)
* 建议配合 [Python virtual env](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) . <i><a href="https://seleniumbase.io/help_docs/virtualenv_instructions/">See shortcut</a>.</i>
* 更新 **[pip](https://pypi.org/project/pip/)** 以防出现警告:

```bash
python -m pip install -U pip
```

<a id="install_seleniumbase"></a>
<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 安装 SeleniumBase:</h2>

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install -r requirements.txt
python setup.py install
```
如果存在多个安装的python版本, 需要显示具体版本 (E.g. 使用 ``python3`` 代替 ``python``).

* 你也可以通过[pypi](https://pypi.python.org/pypi/seleniumbase)安装 ``seleniumbase``  :
```bash
pip install seleniumbase
```
* 添加 ``--upgrade`` 或 ``-U`` 来更新安装程序.
* 添加 ``--force-reinstall`` 更新依赖包.

<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 下载 webdriver:</h3>

SeleniumBase 下载 webdriver 驱动到 [seleniumbase/drivers](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/drivers) 文件夹下, 使用 ``install`` 命令:
```bash
seleniumbase install chromedriver
```
* 你可能需要不同的 webdriver 来对应各种网页浏览器来完成自动化测试,例如: ``chromedriver`` 对应 Chrome, ``edgedriver`` 对应 Edge, ``geckodriver`` 对应 Firefox, ``operadriver`` 对应 Opera,  ``iedriver`` 对应 Internet Explorer.
* 如果你需要安装最新版本的浏览器驱动, 以以下命令获取最新版本浏览器驱动 (<i>因兼容性原因,默认下载的版本为 chromedriver 2.44 </i>):
```bash
seleniumbase install chromedriver latest
```

<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 使用 Chrome 运行用例:</h3>

```bash
cd examples/
pytest my_first_test.py
```
* 如果没指定版本则默认运行的浏览器驱动为 chromedriver, 使用指定版本的命令为: ``--browser=BROWSER``.
* Linux 中 ``--headless`` 为默认值 (无界面运行).你也可以在任何系统中运行无界面模式. 如果你的 Linux服务器有 GUI 界面,你也需要在界面中查看浏览器运行用例的过程,你可以添加 ``--headed`` 或 ``--gui``.

<b>运行 [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) Demo Mode:</b>

```bash
pytest my_first_test.py --demo
```

<img src="https://seleniumbase.io/cdn/gif/my_first_test_1.gif" title="SeleniumBase" />

<b>此处为相关代码 [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py):</b>

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click("link=About")
        self.assert_text("xkcd.com", "h2")
        self.open("://store.xkcd.com/collections/everything")
        self.type("input.search-input", "xkcd book\n")
        self.assert_exact_text("xkcd: volume 0", "h3")
```

* 默认情况下, **[CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp)** 用来查找页面元素.
* 如果你是CSS Selectors新手, 可以通过 [Flukeout](http://flukeout.github.io/) 游戏来帮助学习掌握.
* 在上述代码中可以看到以下相关的 ``SeleniumBase`` 方法:

``from seleniumbase import BaseCase``:

```python
self.open(URL)  # 打开页面
self.click(SELECTOR)  # 点击页面元素
self.type(SELECTOR, TEXT)  # 输入文字 (添加 "\n" 在"TEXT"的末尾来进行换行.)
self.assert_element(SELECTOR)  # 断言元素是否存在并可见
self.assert_text(TEXT)  # 断言文本是否存在并可见 (可以选择某个元素选择器)
self.assert_title(PAGE_TITLE)  # 断言标题是否存在并可见
self.assert_no_404_errors()  # 断言不存在404错误,若存在则断言失败
self.assert_no_js_errors()  # 断言不存在js错误 (Chrome-ONLY)
self.execute_script(JAVASCRIPT)  # 在页面中执行js脚本
self.go_back()  # 返回到上一个url链接页面
self.get_text(SELECTOR)  # 获取元素的文本
self.get_attribute(SELECTOR, ATTRIBUTE)  # 获取某个定位元素的指定元素属性的属性值
self.is_element_visible(SELECTOR)  # 判断元素是否在页面上可见
self.is_text_visible(TEXT)  # 判断文本是否在页面上可见(可提供 SELECTOR)
self.hover_and_click(HOVER_SELECTOR, CLICK_SELECTOR)  # 鼠标移动在指定元素上后点击另一个元素
self.select_option_by_text(DROPDOWN_SELECTOR, OPTION_TEXT)  # 选择下拉框中内容
self.switch_to_frame(FRAME_NAME)  # 切换 webdriver control 到页面上指定 iframe 
self.switch_to_default_content()  # 切换 webdriver control out 到当前的 iframe
self.switch_to_window(WINDOW_NUMBER)  # 切换不同的 window/tab
self.save_screenshot(FILE_NAME)  # 保存当前页面的截图
```

[chinese_test_1.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/translations/chinese_test_1.py):
```python
from seleniumbase.translate.chinese import 硒测试用例

class 我的测试类(硒测试用例):

    def test_例子1(self):
        self.开启网址("https://xkcd.in/comic?lg=cn&id=353")
        self.断言标题("Python - XKCD中文站")
        self.断言元素("#content div.comic-body")
        self.断言文本("上漫画")
        self.单击("div.nextLink")
        self.断言文本("老妈的逆袭", "#content h1")
        self.单击链接文本("下一篇")
        self.断言文本("敲桌子", "#content h1")
        self.断言文本("有时候无聊就是最棒的乐趣")
        self.回去()
        self.单击链接文本("兰德尔·门罗")
        self.断言文本("兰德尔·门罗", "#firstHeading")
        self.更新文本("#searchInput", "程式设计")
        self.单击("#searchButton")
        self.断言文本("程序设计", "#firstHeading")
```

``from seleniumbase.translate.chinese import 硒测试用例``:

```python
self.开启(URL)  # 打开页面
self.单击(SELECTOR)  # 点击页面元素
self.输入文本(SELECTOR, TEXT)  # 输入文字 (添加 "\n" 在"TEXT"的末尾来进行换行.)
self.断言元素(SELECTOR)  # 断言元素是否存在并可见
self.断言文本(TEXT)  # 断言文本是否存在并可见 (可以选择某个元素选择器)
self.断言标题(PAGE_TITLE)  # 断言标题是否存在并可见
self.检查断开的链接()  # 断言不存在404错误,若存在则断言失败
self.检查JS错误()  # 断言不存在js错误 (Chrome-ONLY)
self.执行脚本(JAVASCRIPT)  # 在页面中执行js脚本
self.回去()  # 返回到上一个url链接页面
self.获取文本(SELECTOR)  # 获取元素的文本
self.获取属性(SELECTOR, ATTRIBUTE)  # 获取某个定位元素的指定元素属性的属性值
self.元素是否可见(SELECTOR)  # 判断元素是否在页面上可见
self.文本是否显示(TEXT)  # 判断文本是否在页面上可见(可提供 SELECTOR)
self.悬停并单击(HOVER_SELECTOR, CLICK_SELECTOR)  # 鼠标移动在指定元素上后点击另一个元素
self.按文本选择选项(DROPDOWN_SELECTOR, OPTION_TEXT)  # 选择下拉框中内容
self.切换到帧(FRAME_NAME)  # 切换 webdriver control 到页面上指定 iframe
self.切换到默认内容()  # 切换 webdriver control out 到当前的 iframe
self.切换到窗口(WINDOW_NUMBER)  # 切换不同的 window/tab
self.保存截图(FILE_NAME)  # 保存当前页面的截图
```

完整的 SeleniumBase methods, 可见: <b><a href="https://seleniumbase.io/help_docs/method_summary/">Method Summary</a></b>

<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 了解更多信息:</h2>

<h4>自动化 WebDriver 技能:</h4>
SeleniumBase 自动化控制 WebDriver 操作 web browsers(浏览器),在运行失败后进行截图保存. (<i><a href="https://seleniumbase.io/help_docs/customizing_test_runs/">了解更多关于定制的启动测试用例</a>.</i>)

<h4>简易的代码:</h4>
SeleniumBase 使用简单简约的语法, 例如:

```python
self.type("input", "dogs\n")
```

上述相似的代码在 Webdriver中变现的不是特别好:
(<i>而且下面的代码不包含 SeleniumBase 的智能等待.</i>)

```python
from selenium.webdriver.common.by import By
element = self.driver.find_element(by=By.CSS_SELECTOR, value="input")
element.clear()
element.send_keys("dogs")
element.submit()
```

如你所见,在 WebDriver 中同样的事情并不如 SeleniumBase!
使用 SeleniumBase 让你的用例变得更加简单!
(<i>你可以在你的代码中一直使用 ``self.driver`` .</i>)

<h4>适用 ``pytest`` 或者 ``nosetests`` 在所有的浏览器中运行你的测试用例:</h4>
(<i>推荐使用 **pytest** . **Chrome** 是默认的浏览器.</i>)

```bash
pytest my_first_test.py --browser=chrome

nosetests test_suite.py --browser=firefox
```

Python 文件中所有以 ``test_`` 开头的python方法将自动运行当你使用 ``pytest`` 或 ``nosetests``, (<i>或包含Python文件的文件夹</i>). 还可以使用以下命令更具体地说明在文件中运行什么: (<i>注意，pytest和nosetests的语法是不同的.</i>)

```bash
pytest [FILE_NAME].py::[CLASS_NAME]::[METHOD_NAME]
nosetests [FILE_NAME].py:[CLASS_NAME].[METHOD_NAME]
```

<h4>不再有不可靠的测试:</h4>
在与页面元素进行交互之前，SeleniumBase方法会自动等待页面元素完成加载(*直到超时限制*)。这意味着您不再需要脚本中随机的' time.sleep() '语句.

<h4>自动/手动混合模式:</h4>
SeleniumBase包括一个名为 <b><a href="https://seleniumbase.io/examples/master_qa/ReadMe/">MasterQA</a></b>的解决方案, 通过让自动化执行所有浏览器操作，同时由手动测试人员处理验证，从而加快了手动测试的速度。.

<h4>丰富的特性:</h4>
获取SeleniumBase特性的完整列表, <a href="https://seleniumbase.io/help_docs/features_list/">点击这里</a>.


<a id="detailed_instructions"></a>
<img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290">

<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 详细说明书:</h2>

<h4><b>下面介绍如何在各种web浏览器上运行示例脚本:</b></h4>

首先，为您打算使用的每个浏览器安装一个webdriver:

```bash
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```

接着, 在  **pytest** 和 **nosetests** 中选择一个为您的测试启动器. (<i>可以互换.</i>)

```bash
cd examples/

pytest my_first_test.py --browser=chrome

nosetests my_first_test.py --browser=firefox
```

(<i>如果没有指定浏览器，则默认使用Chrome.</i>)
对于Pytest，绿色的点表示测试通过。“F”表示测试失败。

<a id="seleniumbase_demo_mode"></a> **使用演示模式来帮助您查看所断言的测试.**

如果示例测试运行得太快，您可以在**Demo模式**下运行它，方法是在命令行上添加``--Demo ``，它会在操作之间短暂地暂停浏览器，突出显示正在操作的页面元素，并让您实时了解测试断言的内容::

```bash
pytest my_first_test.py --demo
```

**Pytest** 包括测试发现。如果您没有指定要运行的特定文件或文件夹，`` pytest ``将根据以下匹配条件自动搜索要运行的测试的所有子目录:
Python 文件名应是开头为 ``test_`` 或者以 ``_test.py``结尾.
Python 方法应以 ``test_``开头.
Python类名可以是任何东西，因为SeleniumBase的`` BaseCase ``类继承自`` unittest ``的TestCase的类。
你可以看到哪些测试是由`` pytest ``发现使用::

```bash
pytest --collect-only -q
```

您可以在脚本中使用以下内容来帮助您调试问题:
(<i>如果使用ipdb，请确保将“-s”添加到命令行选项中，除非已经在pytest.ini中</i>)
```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import ipdb; ipdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

<b>要暂停抛出异常或错误的活动测试，请添加``--pdb -s ``:</b>

```bash
pytest my_first_test.py --pdb -s
```

上面的代码将在出现故障时打开浏览器窗口。(ipdb命令:'n'， 'c'， 's' => next, continue, step)。

下面是Pytest附带的一些有用的命令行选项:

```bash
-v  # Prints the full test name for each test.
-q  # Prints fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed pytest-html report after tests finish.
--collect-only  # Show what tests would get run without actually running them.
-n=NUM  # Multithread the tests using that many threads. (Speed up test runs!)
-s  # See print statements. (Should be on by default with pytest.ini present.)
--junit-xml=report.xml  # Creates a junit-xml report after tests finish.
--pdb  # If a test fails, pause run and enter debug mode. (Don't use with CI!)
-m=MARKER  # Only run tests that are marked with the specified pytest marker.
```

SeleniumBase 为测试提供额外的Pytest命令行选项:

```bash
--browser=BROWSER  # (The web browser to use.)
--cap-file=FILE  # (The web browser's desired capabilities to use.)
--cap-string=STRING  # (The web browser's desired capabilities to use.)
--settings-file=FILE  # (Overrides SeleniumBase settings.py values.)
--env=ENV  # (Set a test environment. Use "self.env" to use this in tests.)
--data=DATA  # (Extra data to pass to tests. Use "self.data" in tests.)
--var1=DATA  # (Extra data to pass to tests. Use "self.var1" in tests.)
--var2=DATA  # (Extra data to pass to tests. Use "self.var2" in tests.)
--var3=DATA  # (Extra data to pass to tests. Use "self.var3" in tests.)
--user-data-dir=DIR  # (Set the Chrome user data directory to use.)
--server=SERVER  # (The server / IP address used by the tests.)
--port=PORT  # (The port that's used by the test server.)
--proxy=SERVER:PORT  # (This is the proxy server:port combo used by tests.)
--agent=STRING  # (This designates the web browser's User Agent to use.)
--mobile  # (The option to use the mobile emulator while running tests.)
--metrics=STRING  # ("CSSWidth,Height,PixelRatio" for mobile emulator tests.)
--extension-zip=ZIP  # (Load a Chrome Extension .zip file, comma-separated.)
--extension-dir=DIR  # (Load a Chrome Extension directory, comma-separated.)
--headless  # (The option to run tests headlessly. The default on Linux OS.)
--headed  # (The option to run tests with a GUI on Linux OS.)
--start-page=URL  # (The starting URL for the web browser when tests begin.)
--archive-logs  # (Archive old log files instead of deleting them.)
--time-limit=SECONDS  # (Safely fail any test that exceeds the limit limit.)
--slow  # (The option to slow down the automation.)
--demo  # (The option to visually see test actions as they occur.)
--demo-sleep=SECONDS  # (The option to wait longer after Demo Mode actions.)
--highlights=NUM  # (Number of highlight animations for Demo Mode actions.)
--message-duration=SECONDS  # (The time length for Messenger alerts.)
--check-js  # (The option to check for JavaScript errors after page loads.)
--ad-block  # (The option to block some display ads after page loads.)
--verify-delay=SECONDS  # (The delay before MasterQA verification checks.)
--disable-csp  # (This disables the Content Security Policy of websites.)
--enable-sync  # (The option to enable "Chrome Sync".)
--use-auto-ext  # (The option to use Chrome's automation extension.)
--incognito  #  (The option to enable Chrome's Incognito mode.)
--guest  # (The option to enable Chrome's Guest mode.)
--devtools  # (The option to open Chrome's DevTools when the browser opens.)
--reuse-session  # (The option to reuse the browser session between tests.)
--crumbs  # (Option to delete all cookies between tests reusing a session.)
--maximize-window  # (The option to start with the web browser maximized.)
--save-screenshot  # (The option to save a screenshot after each test.)
--visual-baseline  # (Set the visual baseline for Visual/Layout tests.)
--timeout-multiplier=MULTIPLIER  # (Multiplies the default timeout values.)
```

(有关详细信息，请参见命令行选项的完整列表 **[点击这里](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

在测试失败期间，最近一次测试运行的日志和屏幕截图将被保存到``latest_logs/``文件夹中。如果在命令行选项中添加——archive_logs，或者在 [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)中将``ARCHIVE_EXISTING_LOGS``设置为``True``，那么这些日志将被移动到``archived_logs/``。否则，将在下一次测试运行开始时清理日志文件。``test_suite.py``集合包含故意失败的测试，以便您可以看到日志记录是如何工作的。

```bash
cd examples/

pytest test_suite.py --browser=chrome

pytest test_suite.py --browser=firefox
```

覆盖seleniumbase/config/settings.py的一个简单方法是使用自定义设置文件。下面是要添加到测试中的命令行选项: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings_file=custom_settings.py``
(设置包括默认超时值、双因素auth密钥、DB凭据、S3凭据和测试使用的其他重要设置.)

要将额外的数据从命令行传递给测试，添加 ``--data="ANY STRING"``.
现在在您的测试中，您可以使用 ``self.data`` 来访问。


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 测试目录定制:</h3>

用于在SeleniumBase repo之外运行测试 <b>Pytest</b>, 你需要一份 <b>[pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini)</b> 在根目录上。用于在SeleniumBase repo之外运行测试 <b>Nosetests</b>, 你需要拷贝 <b>[setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg)</b> 在根目录上. (子文件夹应该包括一个空白的 "__init__.py" 文件。)这些文件指定测试的默认配置细节。(对于运行nosetest，还可以使用``--config ``指定.cfg文件。示例`` nosetests [MY_TEST].py--config=[MY_CONFIG].cfg `` ')

作为一个快捷方式，您可以运行`` seleniumbase mkdir [DIRECTORY_NAME] ``来创建一个新的文件夹，其中已经包含了必要的文件和一些可以运行的示例测试。例子:

```bash
seleniumbase mkdir ui_tests
cd ui_tests/
pytest my_first_test.py
```


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 日志记录/失败测试的结果:</h3>

让我们尝试一个失败的测试示例:

```python
""" test_fail.py """
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)  # This should fail
```

你可以运行在``example``文件夹运行:

```bash
pytest test_fail.py
```

您会注意到，创建了一个名为“latest_logs”的日志文件夹来保存有关失败测试的信息和屏幕截图。在测试运行期间，如果您在 [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)中将ARCHIVE_EXISTING_LOGS设置为True, 或者如果您使用``--archive-logs ``运行测试，那么过去的结果就会移动到archived_logs文件夹中。如果您选择不归档现有的日志，它们将被删除，并被最新测试运行的日志所取代。


<a id="creating_visual_reports"></a>
<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 创建可视化测试套件报告:</h3>

(注意:Pytest和nosetest的一些命令行参数是不同的)

<h4><b>Pytest 报告:</b></h4>

使用 ``--html=report.html`` 在您的测试套件完成后，为您提供指定名称的漂亮报告。

```bash
pytest test_suite.py --html=report.html
```

<img src="https://cdn2.hubspot.net/hubfs/100006/images/pytest_report_3c.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

还可以使用``--junit-xml=report``。获取一个xml报告。Jenkins可以使用这个文件为您的测试显示更好的报告。

```bash
pytest test_suite.py --junit-xml=report.xml
```

<h4><b>Nosetest 报告:</b></h4>

 ``--report`` 选项将在测试套件完成后为您提供一个漂亮的报告。

```bash
nosetests test_suite.py --report
```

<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(注意:您可以添加``--show-report ``来在测试套件完成后立即显示Nosetest报告。只在本地运行测试时使用``--show-report ``，因为它会暂停测试运行.)


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 使用代理服务器:</h3>

如果您希望为您的浏览器测试使用代理服务器(仅适用于Chrome和Firefox)，您可以在命令行上添加``--proxy=IP_ADDRESS:PORT ``作为参数。

```bash
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

如果您希望使用的代理服务器需要身份验证，您可以执行以下操作 (Chrome only):

```bash
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

为了使事情更简单，您可以将您经常使用的代理添加到PROXY_LIST中 [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), 然后使用``--proxy=KEY_FROM_PROXY_LIST ``来使用该键的IP_ADDRESS:PORT。

```bash
pytest proxy_test.py --proxy=proxy1
```


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 变更 User-Agent:</h3>

如果您希望为您的浏览器测试更改用户代理(仅限Chrome和Firefox)，您可以在命令行上添加``--agent="USER agent STRING" ``作为参数。

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 为网站建设导游服务:</h3>

学习更多内容 <a href="https://seleniumbase.io/examples/tour_examples/ReadMe/">SeleniumBase Interactive Walkthroughs</a> (在 ``examples/tour_examples`` 文件). 这对于构建一个在线体验网站的原型非常有用。


<a id="utilizing_advanced_features"></a>
<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Production Environments & Integrations:</h3>

下面是为测试设置生产环境时可以做的一些事情:

* 您可以启动 [Jenkins](https://jenkins.io/) 为定期运行测试构建服务器. 这是一个真实的Jenkins的headless浏览器自动化的例子, check out the <a href="https://seleniumbase.io/integrations/azure/jenkins/ReadMe/">SeleniumBase Jenkins在Azure上的例子</a> 或者 <a href="https://seleniumbase.io/integrations/google_cloud/ReadMe/">在谷歌云上的SeleniumBase Jenkins例子</a>.

* 您可以使用 [the Selenium Grid](https://selenium.dev/documentation/en/grid/) 通过在多台机器上并行执行测试来扩展测试. 要做到这一点，请查看 [SeleniumBase selenium_grid folder](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), 这应该有你需要的一切，包括 <a href="https://seleniumbase.io/seleniumbase/utilities/selenium_grid/ReadMe/">Selenium Grid ReadMe</a>, 这会帮助你开始.

* 如果你用 <a href="https://seleniumbase.io/help_docs/mysql_installation/">SeleniumBase MySQL 特性</a> 保存在服务器机器上运行的测试结果,你需要安装 [MySQL Workbench](https://dev.mysql.com/downloads/tools/workbench/) 帮助你从你的数据库更容易地读和写.

* 如果你用 [Slack](https://slack.com), 您可以使用 [Jenkins Slack Plugin](https://github.com/jenkinsci/slack-plugin)很容易地让Jenkins jobs在那里显示结果. 另一种将消息从测试发送到Slack的方法是通过 [Slack's Incoming Webhooks API](https://api.slack.com/incoming-webhooks).

* 如果您正在使用AWS，您可以设置一个 [Amazon S3](https://aws.amazon.com/s3/) 保存来自测试的日志文件和屏幕截图的帐户. 激活此功能, 修改 [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) 连接细节见S3部分, 添加 "``--with-s3-logging``" 在运行测试时使用命令行.

下面是一个启用了附加功能的测试运行示例:

```bash
pytest [YOUR_TEST_FILE].py --with-db-reporting --with-s3-logging
```

<a id="detailed_method_specifications"></a>
<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 详细的方法说明和实例:</h3>

<h4>导航到web页面 (使用相关commands)</h4>

```python
self.open("https://xkcd.com/378/")  # This method opens the specified page.

self.go_back()  # This method navigates the browser to the previous page.

self.go_forward()  # This method navigates the browser forward in history.

self.refresh_page()  # This method reloads the current page.

self.get_current_url()  # This method returns the current page URL.

self.get_page_source()  # This method returns the current page source.
```

<b>ProTip™:</b> 您可能需要使用get_page_source()方法和Python的find()命令来解析源代码，以找到Selenium无法找到的东西。(你可能需要温习一下你的Python编程技能。)

```python
source = self.get_page_source()
head_open_tag = source.find('<head>')
head_close_tag = source.find('</head>', head_open_tag)
everything_inside_head = source[head_open_tag+len('<head>'):head_close_tag]
```

<h4>点击</h4>

单击页面上的元素:

```python
self.click("div#my_id")
```

**ProTip™:** 在大多数web浏览器中，您可以右键单击页面并选择`` Inspect Element ``来查看创建您自己的脚本所需的CSS选择器详细信息.

<h4>输入文本</h4>

self.type(selector, text)  # 用指定的值更新来自指定元素的文本。如果元素丢失或文本字段不可编辑，则引发异常。例如:

```python
self.type("input#id_value", "2012")
```
您也可以使用self.add_text()或WebDriver .send_keys()命令，但是如果文本框中已经有文本，这些命令不会首先清除文本框
如果您想键入特殊的键，这也很容易。这里有一个例子:

```python
from selenium.webdriver.common.keys import Keys
self.find_element("textarea").send_keys(Keys.SPACE + Keys.BACK_SPACE + '\n')  # The backspace should cancel out the space, leaving you with the newline
```

<h4>从页面上的元素获取文本</h4>

```python
text = self.get_text("header h2")
```

<h4>从页面上的元素获取属性值</h4>

```python
attribute = self.get_attribute("#comic img", "title")
```

<h4>断言页面上某个元素在几秒钟内存在:</h4>

```python
self.wait_for_element_present("div.my_class", timeout=10)
```
(注意: 您也可以使用: ``self.assert_element_present(ELEMENT)``)

<h4>在数秒内断言页面上元素的可见性:</h4>

```python
self.wait_for_element_visible("a.my_class", timeout=5)
```
(注意: 这个的简单版本是 ``self.find_element(ELEMENT)`` 和 ``self.assert_element(ELEMENT)``.  find_element() version 返回元素)

由于上面的行返回元素，您可以将其与.click()组合起来，如下所示:

```python
self.find_element("a.my_class", timeout=5).click()

# But you're better off using the following statement, which does the same thing:

self.click("a.my_class")  # DO IT THIS WAY!
```

**ProTip™:** 可以使用点来表示类名(例如:`` div.class_name ``)，这是CSS选择器中`` div[class="class_name"] ``的简化版本。

你也可以使用 ``*=`` 在CSS选择器中搜索任何部分值，如下所示:

```python
self.click('a[name*="partial_name"]')
```

<h4>在数秒内断言页面上元素内的文本的可见性:</h4>

```python
self.assert_text("Make it so!", "div#trek div.picard div.quotes")
self.assert_text("Tea. Earl Grey. Hot.", "div#trek div.picard div.quotes", timeout=3)
```
(注意: ``self.find_text(TEXT, ELEMENT)`` 和 ``self.wait_for_text(TEXT, ELEMENT)`` 干了同一件事. 为了向后字兼容性，保留了较旧的方法名，但默认超时可能不同.)

<h4>断言 anything</h4>

```python
self.assert_true(myvar1 == something)

self.assert_equal(var1, var2)
```

<h4>有用的条件语句 (with creative examples in action)</h4>

is_element_visible(selector)  # is an element visible on a page
```python
if self.is_element_visible('div#warning'):
    print("Red Alert: Something bad might be happening!")
```

is_element_present(selector)  # is an element present on a page
```python
if self.is_element_present('div#top_secret img.tracking_cookie'):
    self.contact_cookie_monster()  # Not a real SeleniumBase method
else:
    current_url = self.get_current_url()
    self.contact_the_nsa(url=current_url, message="Dark Zone Found")  # Not a real SeleniumBase method
```

Another example:
```python
def is_there_a_cloaked_klingon_ship_on_this_page():
    if self.is_element_present("div.ships div.klingon"):
        return not self.is_element_visible("div.ships div.klingon")
    return False
```

is_text_visible(text, selector)  # is text visible on a page
```python
def get_mirror_universe_captain_picard_superbowl_ad(superbowl_year):
    selector = "div.superbowl_%s div.commercials div.transcript div.picard" % superbowl_year
    if self.is_text_visible("For the Love of Marketing and Earl Grey Tea!", selector):
        return "Picard HubSpot Superbowl Ad 2015"
    elif self.is_text_visible("Delivery Drones... Engage", selector):
        return "Picard Amazon Superbowl Ad 2015"
    elif self.is_text_visible("Bing it on Screen!", selector):
        return "Picard Microsoft Superbowl Ad 2015"
    elif self.is_text_visible("OK Glass, Make it So!", selector):
        return "Picard Google Superbowl Ad 2015"
    elif self.is_text_visible("Number One, I've Never Seen Anything Like It.", selector):
        return "Picard Tesla Superbowl Ad 2015"
    elif self.is_text_visible("""With the first link, the chain is forged.
                              The first speech censored, the first thought forbidden,
                              the first freedom denied, chains us all irrevocably.""", selector):
        return "Picard Wikimedia Superbowl Ad 2015"
    elif self.is_text_visible("Let us make sure history never forgets the name ... Facebook", selector):
        return "Picard Facebook Superbowl Ad 2015"
    else:
        raise Exception("Reports of my assimilation are greatly exaggerated.")
```

<h4>切换 tabs</h4>

如果您的测试打开了一个新选项卡/窗口，而现在您有多个页面，该怎么办?没有问题。您需要指定当前想要使用哪个Selenium。在选项卡/窗口之间切换很容易:

```python
self.switch_to_window(1)  # This switches to the new tab (0 is the first one)
```

**ProTip™:** iFrame遵循与新窗口相同的原则—如果要对其中的某些内容采取操作，需要指定iFrame

```python
self.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iFrame
# .... Do something cool (here)
self.switch_to_default_content()  # Exit the iFrame when you're done
```

<h4>处理 Pop-Up 警告</h4>

如果您的测试在浏览器中弹出了一个警告，该怎么办?没有问题。你需要切换到它，要么接受它，要么拒绝它:

```python
self.wait_for_and_accept_alert()

self.wait_for_and_dismiss_alert()
```

如果您不确定在尝试接受或取消警报之前是否有警报，一种处理方法是将警报处理代码包装在try/except块中。其他方法(如.text和.send_keys())也可以使用警报.

<h4>执行定制jQuery脚本:</h4>

Query是一个强大的JavaScript库，允许您在web浏览器中执行高级操作。
如果您所在的web页面已经加载了jQuery，您可以立即开始执行jQuery脚本。
您应该知道这一点，因为web页面在HTML中会包含如下内容:

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
```

如果您想在尚未加载jQuery的页面上使用它，这是可以的。为此，首先运行以下命令:

```python
self.activate_jquery()
```

许多 websites 存在限制 [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) 防止用户将jQuery和其他外部库加载到自己的网站上。如果您需要在这样的网站上使用jQuery或其他JS库，请在命令行上添加``--disable_csp ``。

下面是一些在脚本中使用jQuery的例子:

```python
self.execute_script('jQuery, window.scrollTo(0, 600)')  # Scrolling the page

self.execute_script("jQuery('#annoying-widget').hide()")  # Hiding elements on a page

self.execute_script("jQuery('#hidden-widget').show(0)")  # Showing hidden elements on a page

self.execute_script("jQuery('#annoying-button a').remove()")  # Removing elements on a page

self.execute_script("jQuery('%s').mouseover()" % (mouse_over_item))  # Mouse-over elements on a page

self.execute_script("jQuery('input#the_id').val('my_text')")  # Fast text input on a page

self.execute_script("jQuery('div#dropdown a.link').click()")  # Click elements on a page

self.execute_script("return jQuery('div#amazing')[0].text")  # Returns the css "text" of the element given

self.execute_script("return jQuery('textarea')[2].value")  # Returns the css "value" of the 3rd textarea element on the page
```

在下面的示例中，JavaScript用于在页面上植入代码，然后Selenium可以在此之后访问该页面:

```python
start_page = "https://xkcd.com/465/"
destination_page = "https://github.com/seleniumbase/SeleniumBase"
self.open(start_page)
referral_link = '''<a class='analytics test' href='%s'>Free-Referral Button!</a>''' % destination_page
self.execute_script('''document.body.innerHTML = \"%s\"''' % referral_link)
self.click("a.analytics")  # Clicks the generated button
```
(由于大众需求,这个流量生成示例已经被嵌入到SeleniumBase中 ``self.generate_referral(start_page, end_page)`` 和 ``self.generate_traffic(start_page, end_page, loops)`` 方法中.)

<h4>使用延迟的断言:</h4>

假设您想在单个测试中验证web页面上的多个不同元素，但是您不希望在一次验证多个元素之前测试失败，这样您就不必重新运行测试来查找同一页面上的更多缺失元素。这就是延迟断言的用武之地。这里的例子:

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_delayed_asserts(self):
        self.open('https://xkcd.com/993/')
        self.wait_for_element('#comic')
        self.delayed_assert_element('img[alt="Brand Identity"]')
        self.delayed_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.delayed_assert_element('#comicmap')
        self.delayed_assert_text('Fake Item', '#middleContainer')  # Will Fail
        self.delayed_assert_text('Random', '#middleContainer')
        self.delayed_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_delayed_asserts()
```

``delayed_assert_element()`` 和 ``delayed_assert_text()`` 将保存将引发的任何异常。
要将所有失败的延迟断言清除到单个异常中， 确保在测试方法的末尾调用 ``self.process_delayed_asserts()`` . 如果测试涉及多个页面, 可以在单个页面的所有延迟断言的末尾调用 ``self.process_delayed_asserts()``. 这样，日志文件的屏幕截图就会显示延迟断言的生成位置。

<h4>访问原始WebDriver</h4>

如果您需要访问标准WebDriver附带的任何命令，您可以像这样直接调用它们:

```python
self.driver.delete_all_cookies()
capabilities = self.driver.capabilities
self.driver.find_elements_by_partial_link_text("GitHub")
```
(通常，您会希望在可用时使用带方法的SeleniumBase版本.)

<h4>自动重试失败的测试</h4>

你可以使用 ``--reruns NUM`` 来重试失败的用例,次数为 NUM 值. 使用 ``--reruns-delay SECONDS`` 在重试之间等待那么多秒。例子:

```
pytest --reruns 5 --reruns-delay 1
```

此外，可以使用`` @retry_on_exception() ``装饰器来特别重试失败的方法. (需要 import: ``from seleniumbase import decorators``) 了解更多关于SeleniumBase装饰器的信息, [click here](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/common).


<h3><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> 简讯</h3>

<b>祝贺您开始使用SeleniumBase!</b>

<p>
<div><b>如果你有任何问题，说出来! 并联系我们</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/seleniumbase/SeleniumBase.svg?color=22BB88" title="Closed Issues" /></a>   <a href="https://github.com/seleniumbase/SeleniumBase/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed/seleniumbase/SeleniumBase.svg?logo=github&logoColor=white&color=22BB99" title="Closed Pull Requests" /></a></div>
</p>

<p>
<div><b>如果你喜欢这个项目,请给个❤(stars)吧!</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/stargazers"><img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg?color=888CFA" title="Stargazers" /></a></div>
</p>
<p><div><a href="https://github.com/mdmintz">https://github.com/mdmintz</a></div></p>

<div><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290" /></a></div>

<div><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" title="SeleniumBase" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/releases"><img src="https://img.shields.io/github/repo-size/seleniumbase/seleniumbase.svg" title="SeleniumBase" alt="Repo Size" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase"><img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" title="SeleniumBase" alt="Join the chat!" /></a></div>

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/tested%20with-SeleniumBase-04C38E.svg" alt="Tested with SeleniumBase" /></a> <a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a></div>

<p><div><span><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_github.svg" title="SeleniumBase on GitHub" alt="SeleniumBase on GitHub" width="56" /></a></span>
<span><a href="https://gitter.im/seleniumbase/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_gitter.svg" title="SeleniumBase on Gitter" alt="SeleniumBase on Gitter" width="44" /></a></span>
<span><a href="https://twitter.com/seleniumbase"><img src="https://seleniumbase.io/img/social/share_twitter.svg" title="SeleniumBase on Twitter" alt="SeleniumBase on Twitter" width="60" /></a></span>
<span><a href="https://instagram.com/seleniumbase"><img src="https://seleniumbase.io/img/social/share_instagram.svg" title="SeleniumBase on Instagram" alt="SeleniumBase on Instagram" width="52" /></a></span>
<span><a href="https://www.facebook.com/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_facebook.svg" title="SeleniumBase on Facebook" alt="SeleniumBase on Facebook" width="56" /></a></span></div></p>
