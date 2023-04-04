from seleniumbase import BaseCase


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
            "</ul>\n",
        )
        self.add_slide(
            "<p><b>About me:</b></p>\n"
            "<ul>\n"
            "<li>I created the <b>SeleniumBase</b> framework.</li>\n"
            "<li>I lead the Automation Team at <b>iboss</b>.</li>\n"
            "</ul>\n",
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
            "</ul>\n",
        )
        self.add_slide(
            "<h3>The Format:</h3>"
            "<hr />\n"
            "<ul>\n"
            "<li>Slides.</li>\n"
            "<li>ReadMe files.</li>\n"
            "<li>LOTS of live demos!!!</li>\n"
            "</ul>\n",
            image="https://seleniumbase.io/other/presentation_parts.png",
        )
        self.add_slide(
            "<h3>What does Selenium provide?</h3>\n"
            "<br /><hr /><br />\n"
            "<h4><b>Selenium provides an automation library!</b></h4><br />\n",
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
                "<mark>from selenium import webdriver</mark>\n\n"
                "driver = webdriver.Chrome()\n\n"
                'driver.get("http://selenium.dev")\n\n'
                "element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()\n\n"
                "elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")\n\n'
                "driver.quit()\n\n"
            ),
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "<mark>driver = webdriver.Chrome()</mark>\n\n"
                'driver.get("http://selenium.dev")\n\n'
                "element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()\n\n"
                "elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")\n\n'
                "driver.quit()\n\n"
            ),
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "driver = webdriver.Chrome()\n\n"
                '<mark>driver.get("http://selenium.dev")</mark>\n\n'
                "element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()\n\n"
                "elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")\n\n'
                "driver.quit()\n\n"
            ),
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "driver = webdriver.Chrome()\n\n"
                'driver.get("http://selenium.dev")\n\n'
                "<mark>element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()</mark>\n\n"
                "elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")\n\n'
                "driver.quit()\n\n"
            ),
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "driver = webdriver.Chrome()\n\n"
                'driver.get("http://selenium.dev")\n\n'
                "element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()\n\n"
                "<mark>elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")</mark>\n\n'
                "driver.quit()\n\n"
            ),
        )
        self.add_slide(
            "<h3>What are some building blocks?</h3>\n"
            "<hr /><br />\n",
            code=(
                "from selenium import webdriver\n\n"
                "driver = webdriver.Chrome()\n\n"
                'driver.get("http://selenium.dev")\n\n'
                "element = driver.find_element"
                '("css selector", "#docsearch span")\n\n'
                "element.click()\n\n"
                "elem_2 = driver.find_element"
                '("css selector", "#docsearch-input")\n\n'
                'elem_2.send_keys("Python")\n\n'
                "<mark>driver.quit()</mark>\n\n"
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
            "<br /><br /><br /><br /><br /><br /><br /><br /><br /><br />",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4>\n"
            "<mark>The default timeout is 0: If an element isn't immediately "
            "ready to be interacted with, you'll get errors when trying "
            "to interact with those elements.<mark>\n"
            "</h4>\n",
            image="https://seleniumbase.io/other/messy_stacktrace.png",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4><br />\n"
            "The command statements can get a bit too long:</h4>\n"
            "<p><code><mark>"
            "driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR).click()"
            "</code></mark></p><br />"
            "<h4>This is better:</h4>"
            "<p><code>self.click(CSS_SELECTOR)</code><p><br />",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4><br />\n"
            "The command statements can get a bit too long:</h4>\n"
            "<p><code>"
            "driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR).click()"
            "</code></p><br />"
            "<h4>This is better:</h4>"
            "<p><code><mark>self.click(CSS_SELECTOR)</mark></code><p><br />",
        )
        self.add_slide(
            "<h4>What are some disadvantages of using <b>raw</b> Selenium "
            "without additional libraries or frameworks?</h4><hr />"
            "<h4><mark><br />\n"
            "No HTML reports, dashboards, results, screenshots..."
            "</mark><br /><br />"
            "A test framework can provide those!"
            "<br />",
        )
        self.add_slide(
            "<h5>Raw Selenium disadvantages, continued...</h5><hr />"
            "<h4>\n"
            "No HTML reports, dashboards, results, screenshots..."
            "<br />"
            "<mark>A test framework can provide those!</mark>",
            image="https://seleniumbase.io/cdn/img/dash_report.png",
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
            "</pre>\n"
            "<br />\n"
            "<p>But with a framework:</p>\n"
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
            "</ul>\n",
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
            "<li>Provide test assetions.</li>\n"
            "<li>Multithread your tests.</li>\n"
            "<li>Use a large number of existing plugins.</li>\n"
            "</ul>\n",
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
            "</ul>\n",
        )
        self.add_slide(
            "<h3>How do you get SeleniumBase?</h3>\n"
            "<hr /><br />\n"
            "<h3><code><mark>pip install seleniumbase</mark></code></h3>",
            image="https://seleniumbase.io/other/seleniumbase_github.png",
        )
        self.add_slide(
            "<h2><b>Live Demo Time!</b></h2><hr /><br />"
            "<h3>(Starting with raw Selenium, and evolving that into "
            "SeleniumBase.)</h3>",
            image="https://seleniumbase.io/other/python_3d_logo.png",
        )
        self.begin_presentation(filename="fundamentals.html")
