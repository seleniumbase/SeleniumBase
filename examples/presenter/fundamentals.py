from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_presentation(self):
        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h2>Python Selenium:</h2>\n"
            "<h3>Fundamentals to Frameworks</h3>"
            "<h3>(with SeleniumBase)</h3>\n"
            "<br /><hr /><br />\n"
            "<h3>Presented by <b>Michael Mintz</b></h3>\n"
            "<h3>SeleniumConf 2023 - Chicago</h3>\n"
        )
        self.add_slide(
            "<h3><b>Welcome to Chicago!</b></h3><hr />\n",
            image="https://seleniumbase.io/other/chicago_skyline.png",
        )
        self.add_slide(
            "<h3><b>A few shout-outs before starting:</b></h3><hr /><br />\n"
            "<ul>\n"
            "<li><b>The Selenium Org</b> (made everything possible)</li><br />"
            "<li><b>Conference organizers</b> (made today possible)</li><br />"
            "<li><b>My wife</b> (a major supporter of my work)</li><br />"
            "<li><b>iboss</b> (my employer)</li>\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>About me:</b></p>\n"
            "<ul>\n"
            "<li>I created the <b>SeleniumBase</b> framework.</li>\n"
            "<li>I lead the Automation Team at <b>iboss</b>.</li>\n"
            "</ul>",
            image="https://seleniumbase.io/other/iboss_booth.png",
        )
        self.add_slide(
            "<p><b>"
            "This is the ONLY Python session at SeleniumConf!"
            "</b></p><hr /><br />\n"
            "<h3>\n"
            "If one Python session is not enough, come see me afterwards.\n"
            "</h3>\n",
            image="https://seleniumbase.io/other/python_3d_logo.png",
        )
        self.add_slide(
            "<h4><b>By the end of this presentation, you'll learn:</b></h4>"
            "<hr /><br />\n"
            "<ul>\n"
            "<li>Python Selenium fundamentals.</li><br />\n"
            "<li>How test frameworks can improve on the fundamentals.</li>"
            "<br />\n"
            "<li>How SeleniumBase makes Python Web Automation easier.</li>"
            "<br />\n"
            "</ul>",
        )
        self.add_slide(
            "<h3>The Format:</h3>"
            "<hr />\n"
            "<ul>\n"
            "<li>Slides.</li>\n"
            "<li>ReadMe files.</li>\n"
            "<li>LOTS of live demos!!!</li>\n"
            "</ul>",
            image="https://seleniumbase.io/other/presentation_parts.png",
        )
        self.add_slide(
            "<h3>What does Selenium provide?</h3>\n"
            "<hr /><br />\n"
            "<h4><b>Selenium provides an automation library!</b></h4>\n"
            "<br /><h5>(It does NOT provide a test framework.)</h5>\n",
            image="https://seleniumbase.io/other/selenium_slogan.png",
        )
        self.add_slide(
            "<h3>How do you get Selenium?</h3>\n"
            "<hr />\n"
            "<p>(for Python)</p><br />\n"
            "<h3><code><mark>pip install selenium</mark></code></h3>",
            image="https://seleniumbase.io/other/selenium_pypi.png",
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "<mk-0>from selenium import webdriver</mk-0>\n\n"
                "<mk-1>driver = webdriver.Edge()</mk-1>\n\n"
                '<mk-2>driver.get("http://selenium.dev")</mk-2>\n\n'
                "<mk-3>element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()</mk-3>\n\n"
                "<mk-4>elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")</mk-4>\n\n'
                "<mk-5>driver.quit()</mk-5>\n\n"
            ),
        )
        self.add_slide(
            "<h4>Launching a browser can get more complicated:</h4>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "options = webdriver.ChromeOptions()\n"
                'options.add_argument("--disable-notifications")\n'
                "options.add_experimental_option(\n    "
                '"excludeSwitches", ["enable-automation", "enable-logging"]\n'
                ')\n'
                "prefs = {\n"
                '    "credentials_enable_service": False,\n'
                '    "profile.password_manager_enabled": False,\n'
                "}\n"
                'options.add_experimental_option("prefs", prefs)\n'
                "driver = webdriver.Chrome(options=options)\n"
            ),
        )
        self.add_slide(
            "<h4>Test frameworks wrap Selenium to improve things!</h4><hr />\n"
            "<br />"
            '<a href="https://selenium.dev/documentation/overview/components/'
            '#where-frameworks-fit-in">'
            '(Where does a framework fit in?)</a>\n',
            image="https://seleniumbase.io/other/with_a_framework.png",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4>\n"
            "<br />",
            image="https://seleniumbase.io/other/sel_and_py_2.png",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4>\n"
            "<mark>The default timeout is 0: If an element isn't immediately "
            "ready to be interacted with, you'll get errors when trying "
            "to interact with those elements.</mark>\n"
            "</h4>\n",
            image="https://seleniumbase.io/other/messy_stacktrace.png",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without extra libraries or frameworks?</h4><hr />"
            "<h4><br />\n"
            "The command statements can get a bit too long:</h4>\n"
            "<p><code><mk-0>"
            "driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR).click()"
            "</code></mk-0></p><br />"
            "<h4>This is better:</h4>"
            "<p><code><mk-1>self.click(CSS_SELECTOR)</mk-1></code><p><br />",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4><mark><br />\n"
            "No HTML reports, dashboards, results, screenshots..."
            "</mark><br /><br />A test framework can provide those!<br />",
        )
        self.add_slide(
            "<h5>Raw Selenium disadvantages, continued...<hr />\n"
            "No HTML reports, dashboards, results, screenshots...<div />"
            "<mark>A test framework can provide those!</mark></h5>",
            image="https://seleniumbase.io/cdn/img/dash_report.png",
        )
        self.add_slide(
            "<h4>Raw Selenium disadvantages, continued...</h4><hr />\n"
            "<br />\n"
            "<p><mark>It takes multiple lines of code to do simple tasks:"
            "</mark></p>\n<pre>\n"
            'element = driver.find_element("css selector", "#password")\n'
            "element.clear()\n"
            'element.send_keys("secret_sauce")\n'
            'element.submit()\n'
            "</pre>\n<br />\n"
            "<p>But with a framework, do all that in ONE line:</p>\n"
            '<pre>self.type("#password", "secret_sauce\\n")</pre>'
        )
        self.add_slide(
            "<h4>Raw Selenium disadvantages, continued...</h4><hr />\n"
            "<br />\n"
            "<p>It takes multiple lines of code to do simple tasks:</p>\n"
            "<pre>\n"
            'element = driver.find_element("css selector", "#password")\n'
            "element.clear()\n"
            'element.send_keys("secret_sauce")\n'
            'element.submit()\n'
            "</pre>\n<br />\n"
            "<p><mark>But with a framework, do all that in ONE line:"
            "</mark></p>\n"
            '<pre>self.type("#password", "secret_sauce\\n")</pre>'
        )
        self.add_slide(
            "<h4>What else can test frameworks provide?</h4><hr />\n"
            "<ul>\n"
            "<li>Driver management.</li>\n"
            "<li>Advanced methods. Eg. "
            "<pre>self.assert_no_broken_links()</pre></li>\n"
            "<li>Test assertions. Eg. "
            "<pre>self.assert_text(TEXT, SELECTOR)</pre></li>\n"
            "<li>Command-line options. Eg. "
            "<pre>pytest --browser=edge --html=report.html</pre></li>\n"
            "<li>Advanced tools (Eg. test recorders)</li>\n"
            "<li>Easy to read error messages. Eg. "
            '<pre>Element "h2" was not visible after 10s!</pre></li>'
            "</ul>",
        )
        self.add_slide(
            "<h3>What about test runners?</h3><hr />\n"
            "<h3>Python includes powerful test runners, such as <b>pytest</b>."
            "</h3>\n",
            image="https://seleniumbase.io/other/invoke_pytest.png",
        )
        self.add_slide(
            "<h3>What can <b><code>pytest</code></b> do?</h3><hr />\n"
            "<ul>\n"
            "<li>Auto-collect tests to run.</li>\n"
            "<li>Use markers for organizing tests.</li>\n"
            "<li>Generate test reports.</li>\n"
            "<li>Provide test assertions.</li>\n"
            "<li>Multithread your tests.</li>\n"
            "<li>Use a large number of existing plugins.</li>\n"
            "</ul>",
        )
        self.add_slide(
            "<h4>What about complete frameworks?</h4><hr />\n"
            "<h4><b><code>SeleniumBase</code></b> combines the best of both "
            "<b><code>Selenium</code></b> and <b><code>pytest</code></b> "
            "into a super framework.</h4>\n",
            image="https://seleniumbase.io/cdn/img/sb_logo_10c.png",
        )
        self.add_slide(
            "<h4>SeleniumBase features. <b>(You already saw this slide!)</b>"
            "</h4><hr />\n"
            "<ul>\n"
            "<li>Driver management.</li>\n"
            "<li>Advanced methods. Eg. "
            "<pre>self.assert_no_broken_links()</pre></li>\n"
            "<li>Test assertions. Eg. "
            "<pre>self.assert_text(TEXT, SELECTOR)</pre></li>\n"
            "<li>Command-line options. Eg. "
            "<pre>pytest --browser=edge --html=report.html</pre></li>\n"
            "<li>Advanced tools (Eg. test recorders)</li>\n"
            "<li>Easy to read error messages. Eg. "
            '<pre>Element "h2" was not visible after 10s!</pre></li>'
            "</ul>",
        )
        self.add_slide(
            "<h3>How do you get SeleniumBase?</h3>\n"
            "<hr /><br />\n"
            "<h3><code><mark>pip install seleniumbase</mark></code></h3>",
            image="https://seleniumbase.io/other/seleniumbase_github.png",
        )
        self.add_slide(
            "<h3>SeleniumBase example test:</h3><hr />",
            code=(
                "from seleniumbase import BaseCase\n"
                "BaseCase.main(__name__, __file__)\n\n"
                "class MyTestClass(BaseCase):\n"
                "    def test_basics(self):\n"
                '        self.open("https://www.saucedemo.com")\n'
                '        self.type("#user-name", "standard_user")\n'
                '        self.type("#password", "secret_sauce\\n")\n'
                '        self.assert_element("div.inventory_list")\n'
                '        self.assert_exact_text("Products", "span.title")\n'
                "        self.click('button[name*=\"backpack\"]')\n"
                '        self.click("#shopping_cart_container a")\n'
                '        self.assert_exact_text("Your Cart", "span.title")\n'
                '        self.assert_text("Backpack", "div.cart_item")\n'
                '        self.click("button#checkout")\n'
                '        self.type("#first-name", "SeleniumBase")\n'
                '        self.type("#last-name", "Automation")\n'
                '        self.type("#postal-code", "77123")\n'
                '        self.click("input#continue")\n'
                '        self.assert_text("Checkout: Overview")'
            ),
        )
        self.add_slide(
            "<h3>Common SeleniumBase methods:</h3><hr />",
            code=(
                "self.open(url)  # Navigate the browser window to the URL.\n"
                "self.type(selector, text)  # Update field with the text.\n"
                "self.click(selector)  # Click element with the selector.\n"
                "self.click_link(link_text)  # Click link containing text.\n"
                "self.check_if_unchecked(selector)  # Check checkbox.\n"
                "self.uncheck_if_checked(selector)  # Uncheck checkbox.\n"
                "self.select_option_by_text(dropdown_selector, option)\n"
                "self.hover_and_click(hover_selector, click_selector)\n"
                "self.drag_and_drop(drag_selector, drop_selector)\n"
                "self.choose_file(selector, file_path)  # Upload a file.\n"
                "self.switch_to_frame(frame)  # Switch into the iframe.\n"
                "self.switch_to_default_content()  # Exit all iframes.\n"
                "self.switch_to_parent_frame()  # Exit current iframe.\n"
                "self.open_new_window()  # Open new window in same browser.\n"
                "self.switch_to_window(window)  # Switch to browser window.\n"
                "self.switch_to_default_window()  # Go to original window.\n"
                "self.assert_element(selector)  # Verify element visible.\n"
                "self.assert_text(text, selector)  # Substring assertion.\n"
                "self.assert_exact_text(text, selector)  # String assert."
            ),
        )
        self.add_slide(
            "<h3>Common command-line options:</h3><hr />"
            "<pre>\n"
            '<span class="kwd">--browser=BROWSER</span>'
            '<span class="str">'
            '  (Choose web browser. Default: "chrome".)'
            '</span>\n'
            '<span class="kwd">--edge / --firefox / --safari</span>'
            '<span class="str">'
            '  (Browser Shortcut.)'
            '</span>\n'
            '<span class="kwd">--headless</span>'
            '<span class="str">'
            '  (Run tests headlessly.  Default on Linux OS.)'
            '</span>\n'
            '<span class="kwd">--demo</span>'
            '<span class="str">'
            '  (Slow down and see test actions as they occur.)'
            '</span>\n'
            '<span class="kwd">--slow</span>'
            '<span class="str">'
            '  (Slow down the automation. Faster than Demo Mode.)'
            '</span>\n'
            '<span class="kwd">--reuse-session / --rs</span>'
            '<span class="str">'
            '  (Reuse browser session for tests.)'
            '</span>\n'
            '<span class="kwd">--reuse-class-session / --rcs</span>'
            '<span class="str">'
            '  (RS, but for class tests.)'
            '</span>\n'
            '<span class="kwd">--crumbs</span>'
            '<span class="str">'
            '  (Clear cookies between tests reusing a session.)'
            '</span>\n'
            '<span class="kwd">--maximize</span>'
            '<span class="str">'
            '  (Start tests with the web browser maximized.)'
            '</span>\n'
            '<span class="kwd">--dashboard</span>'
            '<span class="str">'
            '  (Enable the SB Dashboard at dashboard.html)'
            '</span>\n'
            '<span class="kwd">--uc</span>'
            '<span class="str">'
            '  (Enable undetected-chromedriver mode.)'
            '</span>\n'
            '<span class="kwd">--incognito</span>'
            '<span class="str">'
            '  (Enable Incognito mode.)'
            '</span>\n'
            '<span class="kwd">--guest</span>'
            '<span class="str">'
            '  (Enable Guest mode.)'
            '</span>\n'
            '<span class="kwd">-m=MARKER</span>'
            '<span class="str">'
            '  (Run tests with the specified pytest marker.)'
            '</span>\n'
            '<span class="kwd">-n=NUM</span>'
            '<span class="str">'
            '  (Multithread the tests using that many threads.)'
            '</span>\n'
            '<span class="kwd">-v</span>'
            '<span class="str">'
            '  (Verbose mode. Print the full names of each test run.)'
            '</span>\n'
            '<span class="kwd">--html=report.html</span>'
            '<span class="str">'
            '  (Create a detailed pytest-html report.)'
            '</span>\n'
            '<span class="kwd">--collect-only / --co</span>'
            '<span class="str">'
            '  (Only show discovered tests. No run.)'
            '</span>\n'
            '<span class="kwd">--co -q</span>'
            '<span class="str">'
            '  (Only show full names of discovered tests. No run.)'
            '</span>\n'
            '<span class="kwd">-x</span>'
            '<span class="str">'
            '  (Stop running tests after the first failure is reached.)'
            '</span>\n'
            "</pre>"
        )
        self.add_slide(
            "<h3>Common console scripts:</h3><hr />",
            code=(
                "sbase get [DRIVER] [OPTIONS]  # Eg. chromedriver\n"
                "sbase methods  # List common Python methods\n"
                "sbase options  # List common pytest options\n"
                "sbase gui  # Open the SB GUI for pytest\n"
                "sbase caseplans  # Open the SB Case Plans App\n"
                "sbase mkdir [DIRECTORY]  # Create a test directory\n"
                "sbase mkfile [FILE.py]  # Create a test file\n"
                "sbase codegen [FILE.py] [OPTIONS]  # Record a test\n"
                "sbase recorder  # Open the SB Recorder App\n"
                "sbase mkpres  # Create a Presentation boilerplate\n"
                "sbase mkchart  # Create a Chart boilerplate\n"
                "sbase print [FILE]  # Print file to console\n"
                "sbase translate [FILE.py] [OPTIONS]  # Translate\n"
                "sbase extract-objects [SB_FILE.py]  # Get objects\n"
                "sbase inject-objects [SB_FILE.py]  # Swap selectors\n"
                "sbase objectify [SB_FILE.py]  # Get & swap objects\n"
                "sbase revert-objects [SB_FILE.py]  # Undo objectify\n"
                "sbase download server  # Get Selenium Grid JAR file\n"
                "sbase grid-hub [start|stop] [OPTIONS]  # Start Grid\n"
                "sbase grid-node [start|stop] --hub=[IP]  # Add Node"
            ),
        )
        self.add_slide(
            "<h2><b>Live Demo Time!</b></h2><hr /><br />"
            "<h3>(Starting with raw Selenium, and evolving that into "
            "SeleniumBase.)</h3>",
            image="https://seleniumbase.io/other/python_3d_logo.png",
        )
        self.begin_presentation(filename="fundamentals.html")
