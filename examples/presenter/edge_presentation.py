from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--edge", "-s"])


class EdgePresentationClass(BaseCase):
    def test_presentation(self):
        if not self.browser == "edge":
            self.driver.quit()
            self.get_new_driver(browser="edge")
        self.demo_mode = False
        self.maximize_window()
        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h3>A deep dive into:</h3>"
            "<h2>Browser automation</h2>"
            "<h2>on Edge, with Python!</h2>\n"
            "<br /><hr /><br />\n"
            "<h3>Presented by <b>Michael Mintz</b></h3>\n"
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.open("data:,")
        self.open("https://www.bostoncodecamp.com/CC34/Schedule/SessionGrid")
        self.highlight("h2", loops=8)
        if self.is_element_visible('[data-sessionid="467776"]'):
            self.highlight('div[data-sessionid="467776"]', loops=10)
            self.create_tour(theme="driverjs")
            self.add_tour_step(
                "<h2>Here we are</h2>", '[data-sessionid="467776"]'
            )
            self.play_tour()
            self.click('a[onclick*="467776"]')
            self.create_tour(theme="hopscotch")
            self.add_tour_step(
                "<h2>What to expect</h2>",
                "div.sz-modal-session",
                alignment="left",
            )
            self.play_tour()
            self.sleep(0.25)
        self.open("data:,")
        self.create_presentation(theme="beige", transition="fade")
        self.add_slide(
            "<p><b>About the presenter:</b></p>\n"
            "<ul>\n"
            "<li>I created <b>SeleniumBase</b> (for Python).</li>\n"
            "<li>I lead the Automation Team at <b>iboss</b>.</li>\n"
            "</ul>\n",
            image="https://seleniumbase.io/other/iboss_booth.png",
        )
        self.add_slide(
            "<p><b>By the end of this presentation, you'll learn:</b></p>"
            "<hr /><br />\n"
            "<ul>\n"
            "<li>How to automate on Edge using Microsoft's WebDriver.</li>"
            "<br />\n"
            "<li>How Python frameworks can simplify Edge automation.</li>"
            "<br />\n"
            "</ul>\n",
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.open("data:,")
        self.open(
            "https://learn.microsoft.com/en-us/microsoft-edge/"
            "test-and-automation/test-and-automation"
        )
        self.wait_for_element("h1")
        self.sleep(1)
        self.create_tour(theme="default")
        self.add_tour_step("<h1>Let's begin the overview!</h1>")
        self.play_tour()
        if self.is_element_visible('button[data-bi-name="close"]'):
            self.click('button[data-bi-name="close"]')
            self.wait_for_element_not_visible('button[data-bi-name="close"]')
        self.highlight("div.mainContainer")
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", "h1#test-and-automation-in-microsoft-edge", alignment="right"
        )
        self.add_tour_step("", "nav#center-doc-outline ~ p", alignment="right")
        self.add_tour_step(
            "", 'table[aria-label*="Test and automation"]', alignment="right"
        )
        self.add_tour_step("A framework", "#playwright", alignment="left")
        self.add_tour_step("Another framework", "#puppeteer", alignment="left")
        self.add_tour_step("Today's framework", "#webdriver", alignment="left")
        self.add_tour_step(
            "", 'a[href="../webdriver-chromium/"]', alignment="right"
        )
        self.play_tour()
        self.highlight('a:contains("Use WebDriver to automate")')
        self.open(
            "https://learn.microsoft.com/en-us/"
            "microsoft-edge/webdriver-chromium/?tabs=python"
        )
        self.wait_for_element("h1")
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", "#use-webdriver-to-automate-microsoft-edge", alignment="right"
        )
        self.add_tour_step(
            "", 'div[data-heading-level="h2"] ~ p', alignment="right"
        )
        self.add_tour_step(
            "", 'div[data-heading-level="h2"] ~ ul', alignment="right"
        )
        self.add_tour_step(
            "", 'table[aria-label="Table 1"]', alignment="right"
        )
        self.add_tour_step(
            "", "#download-microsoft-edge-webdriver", alignment="right"
        )
        self.add_tour_step(
            "", 'img[src*="microsoft-edge-version"]', alignment="right"
        )
        self.play_tour()
        self.highlight('img[src*="microsoft-edge-version"]')

        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.open("edge://settings/help")
        zoom_in = (
            'img[srcset*="logo"] + div span:nth-of-type(2)'
            '{zoom: 1.5;-moz-transform: scale(1.5);}'
        )
        self.add_css_style(zoom_in)
        self.highlight('div[role="main"]')
        self.highlight('img[srcset*="logo"]')
        self.highlight('img[srcset*="logo"] + div span:nth-of-type(1)')
        self.highlight(
            'img[srcset*="logo"] + div span:nth-of-type(2)', loops=16
        )
        if self.is_element_visible('span[aria-live="assertive"]'):
            self.highlight('span[aria-live="assertive"]', loops=8)
        elif self.is_element_visible('a[href*="fwlink"]'):
            self.highlight('a[href*="fwlink"]', loops=8)
        self.highlight('a[href*="chromium"]')
        self.highlight('a[href*="credits"]')
        self.quit_extra_driver()

        self.switch_to_default_driver()
        self.highlight('img[src*="microsoft-edge-driver-install"]', loops=8)
        self.highlight('p:contains("that matches your version")', loops=8)

        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", '[href*="microsoft-edge/tools/webdriver"]', alignment="right"
        )
        self.play_tour()
        self.highlight('[href*="microsoft-edge/tools/webdriver"]')

        self.get_new_driver(browser="edge", disable_csp=True)
        self.maximize_window()
        self.open(
            "https://developer.microsoft.com/en-us/"
            "microsoft-edge/tools/webdriver/"
        )
        self.wait_for_element("div.common-heading")
        self.scroll_to("div.common-heading")
        zoom_in = 'div.h1{zoom: 1.02;-moz-transform: scale(1.02);}'
        self.add_css_style(zoom_in)
        self.highlight("div.common-heading", loops=8)
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", "div.common-heading", alignment="left"
        )
        self.play_tour()
        self.highlight('div[data-fetch-key="block-web-driver:0"]', loops=12)
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", 'div[data-fetch-key="block-web-driver:0"]', alignment="top"
        )
        self.play_tour()
        self.highlight('div[data-fetch-key="block-web-driver:1"]', loops=12)
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", 'div[data-fetch-key="block-web-driver:1"]', alignment="top"
        )
        self.play_tour()
        self.highlight('section[data-section-id="installation"]', loops=12)
        self.create_tour(theme="driverjs")
        self.add_tour_step(
            "", "div.block-heading--sixtyforty", alignment="left"
        )
        self.play_tour()
        self.quit_extra_driver()

        self.switch_to_default_driver()
        self.create_tour(theme="hopscotch")
        self.add_tour_step(
            "", 'img[src*="microsoft-edge-driver-install"]', alignment="left"
        )
        self.play_tour()
        self.highlight('p:contains("After the download completes")', loops=10)
        self.sleep(0.5)

        self.create_tour(theme="hopscotch")
        self.add_tour_step(
            "", "#choose-a-webdriver-testing-framework", alignment="left"
        )
        self.add_tour_step("", "#using-selenium-4", alignment="left")
        self.add_tour_step(
            "", "#automate-microsoft-edge-with-webdriver", alignment="left"
        )
        self.add_tour_step("", "#automate-microsoft-edge", alignment="left")
        self.add_tour_step("", "#tabgroup_1", alignment="left")
        self.add_tour_step(
            "", '[id*="configure-the-edge-webdriver-serv"]', alignment="left"
        )
        self.add_tour_step("", "#tabgroup_2", alignment="left")
        self.add_tour_step(
            "", "#configure-microsoft-edge-options", alignment="left"
        )
        self.add_tour_step(
            "", "#choose-specific-browser-binaries", alignment="left"
        )
        self.add_tour_step("", "#tabgroup_3", alignment="left")
        self.add_tour_step(
            "", "#pass-extra-command-line-arguments", alignment="left"
        )
        self.add_tour_step("", "#tabgroup_4", alignment="left")
        self.add_tour_step(
            "", "#other-webdriver-installation-options", alignment="left"
        )
        self.add_tour_step(
            "", 'code[data-author-content*="docker run"]', alignment="left"
        )
        self.add_tour_step(
            "", "#opt-out-of-diagnostic-data-collection", alignment="left"
        )
        self.add_tour_step(
            "", "#developer-tools-availability-policy", alignment="left"
        )
        self.play_tour()
        self.sleep(0.25)
        self.open("data:,")

        self.create_presentation(theme="sky", transition="fade")
        self.add_slide(
            "<p>How do you get Selenium?</p>\n"
            "<hr />\n"
            "<p>(for Python)</p><br />\n"
            "<h3><code><mark>pip install selenium</mark></code></h3>",
            image="https://seleniumbase.io/other/selenium_pypi.png",
        )
        self.add_slide(
            "<p>What are some building blocks?</p>\n"
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
            "<p>Is Selenium really a framework, or just a library?</p>\n"
            "<hr /><br />\n"
            "<p>Given that Selenium uses WebDriver APIs for interacting with"
            " websites, but lacks essential features for structuring tests,"
            " (and more...), Selenium is really: JUST A LIBRARY!</p>\n",
            image="https://seleniumbase.io/other/selenium_slogan.png"
        )
        self.add_slide(
            "<p>JUST A LIBRARY, continued...</p>\n"
            "<hr /><br />\n"
            "<p>Technically, Selenium consists of multiple language bindings"
            " for interacting with WebDriver APIs. These bindings include:"
            " C#, Java, JS, Python, and Ruby.</p>\n",
            image="https://seleniumbase.io/other/library_books.jpg"
        )
        self.add_slide(
            "<p>Test frameworks wrap Selenium to improve things!</p><hr />\n"
            "<br />"
            '<a href="https://selenium.dev/documentation/overview/components/'
            '#where-frameworks-fit-in">'
            '(Where does a framework fit in?)</a>\n',
            image="https://seleniumbase.io/other/with_a_framework.png",
        )
        self.add_slide(
            "<p>What are some disadvantages of using <b>raw</b> Selenium "
            "without extra libraries or frameworks?</h4><hr />"
            "<p>\n"
            "<br />",
            image="https://seleniumbase.io/other/sel_and_py_2.png",
        )
        self.add_slide(
            "<p>What are some disadvantages of using <b>raw</b> Selenium "
            "without extra libraries or frameworks?</p><hr />"
            "<p>\n"
            "<mark>The default timeout is 0: If an element isn't immediately "
            "ready to be interacted with, you'll get errors when trying "
            "to interact with those elements.</mark>\n"
            "</p>\n",
            image="https://seleniumbase.io/other/messy_stacktrace.png",
        )
        self.add_slide(
            "<p>What are some disadvantages of using <b>raw</b> Selenium "
            "without extra libraries or frameworks?</p><hr />"
            "<p><br />\n"
            "The command statements can get a bit too long:</p>\n"
            "<p><code><mk-0>"
            "driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR).click()"
            "</code></mk-0></p><br />"
            "<p>This is better:</p>"
            "<p><code><mk-1>self.click(CSS_SELECTOR)</mk-1></code><p><br />",
        )
        self.add_slide(
            "<p>What are some disadvantages of using <b>raw</b> Selenium "
            "without extra libraries or frameworks?</p><hr /><br />\n"
            "<mark>No HTML reports, dashboards, screenshots...</mark><br />"
            "<p>A test framework can provide those!</p><br />",
        )
        self.add_slide(
            "<h6>Raw Selenium disadvantages, continued...</h6><hr />"
            "<h6>No HTML reports, dashboards, screenshots...</h6>\n"
            "<mark>A test framework can provide those!</mark>",
            image="https://seleniumbase.io/cdn/img/dash_report.png",
        )
        self.add_slide(
            "<p>Raw Selenium disadvantages, continued...</p><hr />\n<br />\n"
            "<p><mk-0>It takes multiple lines of code to do simple tasks:"
            "</mk-0></p>\n<pre>\n"
            'element = driver.find_element("css selector", "#password")\n'
            "element.clear()\n"
            'element.send_keys("secret_sauce")\n'
            'element.submit()\n'
            "</pre>\n<br />\n"
            "<p><mk-1>But with a framework, do all that in ONE line:</mk-1>"
            '</p>\n<pre>self.type("#password", "secret_sauce\\n")</pre>'
        )
        self.add_slide(
            "<p>What else can test frameworks provide?</p><hr />\n"
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
            "<p>What about test runners?</p><hr />\n"
            "<p>Python includes powerful test runners, such as <b>pytest</b>."
            "</p>\n",
            image="https://seleniumbase.io/other/invoke_pytest.png",
        )
        self.add_slide(
            "<p>What can <b><code>pytest</code></b> do?</p><hr />\n"
            "<ul>\n"
            "<li>Auto-collect tests to run.</li>\n"
            "<li>Use markers for organizing tests.</li>\n"
            "<li>Generate test reports.</li>\n"
            "<li>Provide test assertions.</li>\n"
            "<li>Multithread your tests.</li>\n"
            "<li>Use a large number of existing plugins.</li>\n"
            "</ul>\n",
        )
        self.add_slide(
            "<p>What about complete frameworks?</p><hr />\n"
            "<p><b><code>SeleniumBase</code></b> combines the best of both "
            "<b><code>Selenium</code></b> and <b><code>pytest</code></b> "
            "into a super framework.</p>\n",
            image="https://seleniumbase.io/cdn/img/sb_logo_10c.png",
        )
        self.add_slide(
            "<p>SeleniumBase features. <b>(You already saw this!)</b>"
            "</p><hr />\n"
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
            "<p>How do you get SeleniumBase?</p>\n"
            "<hr /><br />\n"
            "<h3><code><mark>pip install seleniumbase</mark></code></h3>",
            image="https://seleniumbase.io/other/seleniumbase_github.png",
        )
        code = (
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
        )
        self.add_slide(
            "SeleniumBase example test<hr />",
            code=code,
        )
        self.add_slide(
            "SeleniumBase example test <mark>(Time to run this!)</mark><hr />",
            code=code,
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)

        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.open("data:,")
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_exact_text("Products", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("Your Cart", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#checkout")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Automation")
        self.type("#postal-code", "77123")
        self.click("input#continue")
        self.assert_text("Checkout: Overview")
        self.quit_extra_driver()

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            '<mark>(Now to run that same test in "--demo" mode!)</mark><hr />',
            code=code,
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.open("data:,")
        self.demo_mode = True
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_exact_text("Products", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("Your Cart", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#checkout")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Automation")
        self.type("#postal-code", "77123")
        self.click("input#continue")
        self.assert_text("Checkout: Overview")
        self.demo_mode = False
        self.quit_extra_driver()

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h3>What about Edge tests using a mobile emulator?</h3><hr />"
            "<br /><h3><code><mark>pytest --edge --mobile</mark></code></h3>"
            "<br /><h3>Another demo...</h3>",
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.get_new_driver(browser="edge", is_mobile=True)
        self.maximize_window()
        self.open("https://www.skype.com/en/get-skype/")
        self.assert_element('[aria-label="Microsoft"]')
        self.assert_text("Download Skype", "h1")
        self.highlight("div.appBannerContent")
        self.highlight("h1")
        self.assert_text("Skype for Mobile", "h2")
        self.highlight("h2")
        self.highlight("#get-skype-0")
        self.highlight_click("span[data-dropdown-icon]")
        self.highlight("#get-skype-0_android-download")
        self.highlight('[data-bi-id*="ios"]')
        self.quit_extra_driver()

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h3>What about 2-Factor Auth?</h3><hr /><br />\n"
            "<br /><h3>Another demo...</h3>",
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.demo_mode = True
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
        self.assert_text("Welcome!", "h1")
        self.highlight("img#image1")  # A fancier assert_element() call
        self.click('a:contains("This Page")')  # Use :contains() on any tag
        self.save_screenshot_to_logs()  # ("./latest_logs" folder for test)
        self.click_link("Sign out")  # Link must be "a" tag. Not "button".
        self.assert_element('a:contains("Sign in")')
        self.assert_exact_text("You have been signed out!", "#top_message")
        self.demo_mode = False
        self.quit_extra_driver()

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h2>Need some coffee?<h2><hr /><br />\n"
            "<h2>Another demo...</h2>",
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.demo_mode = True
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-sb="Cappuccino"]')
        self.click('div[data-sb="Flat-White"]')
        self.click('div[data-sb="Cafe-Latte"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $53.00", "button.pay")
        self.click("button.pay")
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "#app .success")
        self.demo_mode = False
        self.quit_extra_driver()

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h3>Let's have some fun!</h3><hr /><br />\n"
            "<br /><h3>Another demo...</h3>",
        )
        self.begin_presentation(filename="edge_presentation.html")
        self.sleep(0.25)
        self.get_new_driver(browser="edge")
        self.maximize_window()
        self.open("https://seleniumbase.io/error_page/")
        self.highlight('img[alt="500 Error"]')
        self.highlight("img#parallax_octocat")
        self.highlight("#parallax_error_text")
        self.highlight('img[alt*="404"]')
        self.highlight("img#octobi_wan_catnobi")
        self.highlight("img#speeder")
        self.quit_extra_driver()
        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h2>Let's learn more...</h2><hr /><br />\n"
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
            '<span class="kwd">--rs / --reuse-session</span>'
            '<span class="str">'
            '  (Reuse browser session for tests.)'
            '</span>\n'
            '<span class="kwd">--rcs / --reuse-class-session</span>'
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
            '<span class="kwd">--co / --collect-only</span>'
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
            "<h3><b>Live Demo Time!</b></h3><hr />"
            "<h3>(Let's head over to GitHub...)</h3>",
            image="https://seleniumbase.io/other/sbase_qr_code_s.png",
        )
        self.begin_presentation(filename="edge_presentation.html")
