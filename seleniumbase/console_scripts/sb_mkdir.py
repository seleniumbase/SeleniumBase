# -*- coding: utf-8 -*-
"""
Creates a new folder for running SeleniumBase scripts.

Usage:
    seleniumbase mkdir [DIRECTORY] [OPTIONS]
    OR     sbase mkdir [DIRECTORY] [OPTIONS]

Example:
    sbase mkdir ui_tests

Options:
    -b / --basic  (Only config files. No tests added.)

Output:
    Creates a new folder for running SBase scripts.
    The new folder contains default config files,
    sample tests for helping new users get started,
    and Python boilerplates for setting up customized
    test frameworks.
"""

import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = ("  ** mkdir **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase mkdir [DIRECTORY] [OPTIONS]\n"
    exp += "          OR     sbase mkdir [DIRECTORY] [OPTIONS]\n"
    exp += "  Example:\n"
    exp += "          sbase mkdir ui_tests\n"
    exp += "  Options:\n"
    exp += "          -b / --basic  (Only config files. No tests added.)\n"
    exp += "  Output:\n"
    exp += "          Creates a new folder for running SBase scripts.\n"
    exp += "          The new folder contains default config files,\n"
    exp += "          sample tests for helping new users get started,\n"
    exp += "          and Python boilerplates for setting up customized\n"
    exp += "          test frameworks.\n"
    if not msg:
        raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)
    elif msg == "help":
        print("\n%s" % exp)
        sys.exit()
    else:
        raise Exception('INVALID RUN COMMAND!\n\n%s\n%s\n' % (exp, msg))


def main():
    c1 = ""
    c5 = ""
    c7 = ""
    cr = ""
    if "linux" not in sys.platform:
        colorama.init(autoreset=True)
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL

    basic = False
    help_me = False
    error_msg = None
    invalid_cmd = None

    command_args = sys.argv[2:]
    dir_name = command_args[0]
    if dir_name == "-h" or dir_name == "--help":
        invalid_run_command("help")
    elif len(str(dir_name)) < 2:
        error_msg = (
            'Directory name length must be at least 2 characters long!')
    elif "/" in str(dir_name) or "\\" in str(dir_name):
        error_msg = (
            'Directory name must not include slashes ("/", "\\")!')
    elif dir_name.startswith("-"):
        error_msg = 'Directory name cannot start with "-"!'
    elif os.path.exists(os.getcwd() + '/' + dir_name):
        error_msg = (
            'Directory "%s" already exists in this directory!' % dir_name)
    if error_msg:
        error_msg = c5 + "ERROR: " + error_msg + cr
        invalid_run_command(error_msg)

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "-h" or option == "--help":
                help_me = True
            elif option == "-b" or option == "--basic":
                basic = True
            else:
                invalid_cmd = "\n===> INVALID OPTION: >> %s <<\n" % option
                invalid_cmd = invalid_cmd.replace('>> ', ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(' <<', " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace('>>', c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace('<<', c7 + "<<" + cr)
                help_me = True
                break
    if help_me:
        invalid_run_command(invalid_cmd)

    os.mkdir(dir_name)

    data = []
    seleniumbase_req = "seleniumbase"
    try:
        from seleniumbase import __version__
        seleniumbase_req = "seleniumbase>=%s" % str(__version__)
    except Exception:
        pass
    data.append(seleniumbase_req)
    data.append("")
    file_path = "%s/%s" % (dir_name, "requirements.txt")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("[pytest]")
    data.append("addopts = --capture=no --ignore conftest.py "
                "-p no:cacheprovider")
    data.append("filterwarnings =")
    data.append("    ignore::pytest.PytestWarning")
    data.append("    ignore:.*U.*mode is deprecated:DeprecationWarning")
    data.append("junit_family = legacy")
    data.append("python_files = test_*.py *_test.py *_tests.py *_suite.py")
    data.append("python_classes = Test* *Test* *Test *Tests *Suite")
    data.append("python_functions = test_*")
    data.append("markers =")
    data.append("    marker1: custom marker")
    data.append("    marker2: custom marker")
    data.append("    marker3: custom marker")
    data.append("    marker_test_suite: custom marker")
    data.append("    expected_failure: custom marker")
    data.append("    local: custom marker")
    data.append("    remote: custom marker")
    data.append("    offline: custom marker")
    data.append("    develop: custom marker")
    data.append("    qa: custom marker")
    data.append("    ci: custom marker")
    data.append("    e2e: custom marker")
    data.append("    ready: custom marker")
    data.append("    smoke: custom marker")
    data.append("    deploy: custom marker")
    data.append("    active: custom marker")
    data.append("    master: custom marker")
    data.append("    release: custom marker")
    data.append("    staging: custom marker")
    data.append("    production: custom marker")
    data.append("")
    file_path = "%s/%s" % (dir_name, "pytest.ini")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("[nosetests]")
    data.append("nocapture=1")
    data.append("logging-level=INFO")
    data.append("")
    data.append("[bdist_wheel]")
    data.append("universal=1")
    file_path = "%s/%s" % (dir_name, "setup.cfg")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("")
    file_path = "%s/%s" % (dir_name, "__init__.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("*.py[cod]")
    data.append("*.egg")
    data.append("*.egg-info")
    data.append("dist")
    data.append("build")
    data.append("ghostdriver.log")
    data.append("eggs")
    data.append("parts")
    data.append("bin")
    data.append("var")
    data.append("sdist")
    data.append("develop-eggs")
    data.append(".installed.cfg")
    data.append("lib")
    data.append("lib64")
    data.append("__pycache__")
    data.append(".env")
    data.append(".venv")
    data.append("env/")
    data.append("venv/")
    data.append("ENV/")
    data.append("VENV/")
    data.append("env.bak/")
    data.append("venv.bak/")
    data.append("sbase")
    data.append("sbase*")
    data.append("seleniumbase_env")
    data.append("seleniumbase_venv")
    data.append("sbase_env")
    data.append("sbase_venv")
    data.append("pyvenv.cfg")
    data.append(".Python")
    data.append("include")
    data.append("pip-delete-this-directory.txt")
    data.append("pip-selfcheck.json")
    data.append("ipython.1.gz")
    data.append("nosetests.1")
    data.append("pip-log.txt")
    data.append(".swp")
    data.append(".coverage")
    data.append(".tox")
    data.append("coverage.xml")
    data.append("nosetests.xml")
    data.append(".cache/*")
    data.append(".pytest_cache/*")
    data.append(".pytest_config")
    data.append("junit")
    data.append("test-results.xml")
    data.append(".idea")
    data.append(".project")
    data.append(".pydevproject")
    data.append(".vscode")
    data.append("chromedriver")
    data.append("geckodriver")
    data.append("msedgedriver")
    data.append("operadriver")
    data.append("MicrosoftWebDriver.exe")
    data.append("IEDriverServer.exe")
    data.append("chromedriver.exe")
    data.append("geckodriver.exe")
    data.append("msedgedriver.exe")
    data.append("operadriver.exe")
    data.append("logs")
    data.append("latest_logs")
    data.append("log_archives")
    data.append("archived_logs")
    data.append("geckodriver.log")
    data.append("pytestdebug.log")
    data.append("latest_report")
    data.append("report_archives")
    data.append("archived_reports")
    data.append("html_report.html")
    data.append("report.html")
    data.append("report.xml")
    data.append("dashboard.html")
    data.append("allure_report")
    data.append("allure-report")
    data.append("allure_results")
    data.append("allure-results")
    data.append("saved_charts")
    data.append("saved_presentations")
    data.append("tours_exported")
    data.append("images_exported")
    data.append("saved_cookies")
    data.append("visual_baseline")
    data.append("selenium-server-standalone.jar")
    data.append("proxy.zip")
    data.append("verbose_hub_server.dat")
    data.append("verbose_node_server.dat")
    data.append("ip_of_grid_hub.dat")
    data.append("downloaded_files")
    data.append("archived_files")
    data.append("assets")
    data.append("temp")
    data.append("temp_*/")
    data.append("node_modules")
    file_path = "%s/%s" % (dir_name, ".gitignore")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    if basic:
        success = (
            '\n' + c1 + '* Directory "' + dir_name + '" was created '
            'with config files! *' + cr + '\n')
        print(success)
        return

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class MyTestClass(BaseCase):")
    data.append("")
    data.append("    def test_basics(self):")
    data.append('        url = "https://store.xkcd.com/collections/posters"')
    data.append("        self.open(url)")
    data.append("        self.type('input[name=\"q\"]', \"xkcd book\")")
    data.append("        self.click('input[value=\"Search\"]')")
    data.append('        self.assert_text("xkcd: volume 0", "h3")')
    data.append('        self.open("https://xkcd.com/353/")')
    data.append('        self.assert_title("xkcd: Python")')
    data.append("        self.assert_element('img[alt=\"Python\"]')")
    data.append("        self.click('a[rel=\"license\"]')")
    data.append('        self.assert_text("free to copy and reuse")')
    data.append('        self.go_back()')
    data.append('        self.click_link("About")')
    data.append('        self.assert_exact_text("xkcd.com", "h2")')
    data.append("")
    file_path = "%s/%s" % (dir_name, "my_first_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class DemoSiteTests(BaseCase):")
    data.append("")
    data.append("    def test_demo_site(self):")
    data.append('        self.open("https://seleniumbase.io/demo_page.html")')
    data.append('        self.assert_title("Web Testing Page")')
    data.append('        self.assert_element("tbody#tbodyId")')
    data.append('        self.assert_text("Demo Page", "h1")')
    data.append('        self.type("#myTextInput", "This is Automated")')
    data.append('        self.type("textarea.area1", "Testing Time!\\n")')
    data.append("        self.type('[name=\"preText2\"]', \"Typing Text!\")")
    data.append('        self.assert_text("Automation Practice", "h3")')
    data.append('        self.hover_and_click("#myDropdown", "#dropOption2")')
    data.append('        self.assert_text("Link Two Selected", "h3")')
    data.append('        self.assert_text("This Text is Green", "#pText")')
    data.append('        self.click("#myButton")')
    data.append('        self.assert_text("This Text is Purple", "#pText")')
    data.append("        self.assert_element('svg[name=\"svgName\"]')")
    data.append("        self.assert_element('progress[value=\"50\"]')")
    data.append('        self.press_right_arrow("#myslider", times=5)')
    data.append("        self.assert_element('progress[value=\"100\"]')")
    data.append("        self.assert_element('meter[value=\"0.25\"]')")
    data.append('        self.select_option_by_text("#mySelect", '
                '"Set to 75%")')
    data.append("        self.assert_element('meter[value=\"0.75\"]')")
    data.append('        self.assert_false(self.is_element_visible("img"))')
    data.append('        self.switch_to_frame("#myFrame1")')
    data.append('        self.assert_true(self.is_element_visible("img"))')
    data.append('        self.switch_to_default_content()')
    data.append('        self.assert_false(self.is_text_visible('
                '"iFrame Text"))')
    data.append('        self.switch_to_frame("#myFrame2")')
    data.append('        self.assert_true(self.is_text_visible('
                '"iFrame Text"))')
    data.append('        self.switch_to_default_content()')
    data.append('        self.assert_false(self.is_selected("#radioButton2"))')
    data.append('        self.click("#radioButton2")')
    data.append('        self.assert_true(self.is_selected("#radioButton2"))')
    data.append('        self.assert_false(self.is_selected("#checkBox1"))')
    data.append('        self.click("#checkBox1")')
    data.append('        self.assert_true(self.is_selected("#checkBox1"))')
    data.append('        self.assert_false(self.is_selected("#checkBox2"))')
    data.append('        self.assert_false(self.is_selected("#checkBox3"))')
    data.append('        self.assert_false(self.is_selected("#checkBox4"))')
    data.append('        self.click_visible_elements("input.checkBoxClassB")')
    data.append('        self.assert_true(self.is_selected("#checkBox2"))')
    data.append('        self.assert_true(self.is_selected("#checkBox3"))')
    data.append('        self.assert_true(self.is_selected("#checkBox4"))')
    data.append('        self.assert_false(self.is_element_visible(".fBox"))')
    data.append('        self.switch_to_frame("#myFrame3")')
    data.append('        self.assert_true(self.is_element_visible(".fBox"))')
    data.append('        self.assert_false(self.is_selected(".fBox"))')
    data.append('        self.click(".fBox")')
    data.append('        self.assert_true(self.is_selected(".fBox"))')
    data.append('        self.switch_to_default_content()')
    data.append('        self.assert_link_text("seleniumbase.com")')
    data.append('        self.assert_link_text("SeleniumBase on GitHub")')
    data.append('        self.assert_link_text("seleniumbase.io")')
    data.append('        self.click_link("SeleniumBase Demo Page")')
    data.append('        self.assert_exact_text("Demo Page", "h1")')
    data.append('        self.highlight("h2")')
    data.append("")
    file_path = "%s/%s" % (dir_name, "test_demo_site.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("from parameterized import parameterized")
    data.append("")
    data.append("")
    data.append("class GoogleTests(BaseCase):")
    data.append("")
    data.append("    @parameterized.expand([")
    data.append('        ["pypi", "pypi.org"],')
    data.append('        ["wikipedia", "wikipedia.org"],')
    data.append('        ["seleniumbase", "seleniumbase/SeleniumBase"],')
    data.append("    ])")
    data.append("    def test_parameterized_google_search("
                "self, search_term, expected_text):")
    data.append("        self.open('https://google.com/ncr')")
    data.append("        self.type('input[title=\"Search\"]', "
                "search_term + '\\n')")
    data.append("        self.assert_element('#result-stats')")
    data.append("        self.assert_text(expected_text, '#search')")
    data.append("")
    file_path = "%s/%s" % (dir_name, "parameterized_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    dir_name_2 = dir_name + "/" + "boilerplates"
    os.mkdir(dir_name_2)

    data = []
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "__init__.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class BaseTestCase(BaseCase):")
    data.append("")
    data.append("    def setUp(self):")
    if sys.version_info[0] >= 3:
        data.append("        super().setUp()")
    else:
        data.append("        super(BaseTestCase, self).setUp()")
    data.append("        # <<< Run custom code AFTER the super() line >>>")
    data.append("")
    data.append("    def tearDown(self):")
    data.append("        self.save_teardown_screenshot()")
    data.append("        if self.has_exception():")
    data.append("            # <<< Run custom code if the test failed. >>>")
    data.append("            pass")
    data.append("        else:")
    data.append("            # <<< Run custom code if the test passed. >>>")
    data.append("            pass")
    data.append("        # (Wrap unreliable code in a try/except block.)")
    data.append("        # <<< Run custom code BEFORE the super() line >>>")
    if sys.version_info[0] >= 3:
        data.append("        super().tearDown()")
    else:
        data.append("        super(BaseTestCase, self).tearDown()")
    data.append("")
    data.append("    def login(self):")
    data.append("        # <<< Placeholder. Add your code here. >>>")
    data.append("        pass")
    data.append("")
    data.append("    def example_method(self):")
    data.append("        # <<< Placeholder. Add your code here. >>>")
    data.append("        pass")
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "base_test_case.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("class Page(object):")
    data.append('    html = "html"')
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "page_objects.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from .base_test_case import BaseTestCase")
    data.append("from .page_objects import Page")
    data.append("")
    data.append("")
    data.append("class MyTestClass(BaseTestCase):")
    data.append("")
    data.append("    def test_boilerplate(self):")
    data.append("        self.login()")
    data.append("        self.example_method()")
    data.append("        self.assert_element(Page.html)")
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "boilerplate_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class DataPage():")
    data.append("")
    data.append("    def go_to_data_url(self, sb):")
    data.append('        sb.open("data:text/html,<p>Hello!</p><input />")')
    data.append("")
    data.append("    def add_input_text(self, sb, text):")
    data.append('        sb.type("input", text)')
    data.append("")
    data.append("")
    data.append("class ObjTests(BaseCase):")
    data.append("")
    data.append("    def test_data_url_page(self):")
    data.append("        DataPage().go_to_data_url(self)")
    data.append('        self.assert_text("Hello!", "p")')
    data.append('        DataPage().add_input_text(self, "Goodbye!")')
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "classic_obj_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("class DataPage():")
    data.append("")
    data.append("    def go_to_data_url(self, sb):")
    data.append('        sb.open("data:text/html,<p>Hello!</p><input />")')
    data.append("")
    data.append("    def add_input_text(self, sb, text):")
    data.append('        sb.type("input", text)')
    data.append("")
    data.append("")
    data.append("class ObjTests():")
    data.append("")
    data.append("    def test_data_url_page(self, sb):")
    data.append("        DataPage().go_to_data_url(sb)")
    data.append('        sb.assert_text("Hello!", "p")')
    data.append('        DataPage().add_input_text(sb, "Goodbye!")')
    data.append("")
    file_path = "%s/%s" % (dir_name_2, "sb_fixture_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    dir_name_3 = dir_name_2 + "/" + "samples"
    os.mkdir(dir_name_3)

    data = []
    data.append("")
    file_path = "%s/%s" % (dir_name_3, "__init__.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("from .google_objects import HomePage, ResultsPage")
    data.append("")
    data.append("")
    data.append("class GoogleTests(BaseCase):")
    data.append("")
    data.append("    def test_google_dot_com(self):")
    data.append("        self.open('https://google.com/ncr')")
    data.append("        self.type(HomePage.search_box, 'github')")
    data.append("        self.assert_element(HomePage.list_box)")
    data.append("        self.assert_element(HomePage.search_button)")
    data.append(
        "        self.assert_element(HomePage.feeling_lucky_button)")
    data.append("        self.click(HomePage.search_button)")
    data.append(
        "        self.assert_text('github.com', "
        "ResultsPage.search_results)")
    data.append("        self.assert_element(ResultsPage.images_link)")
    data.append("")
    file_path = "%s/%s" % (dir_name_3, "google_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("class HomePage(object):")
    data.append("    dialog_box = '[role=\"dialog\"] div'")
    data.append("    search_box = 'input[title=\"Search\"]'")
    data.append("    list_box = '[role=\"listbox\"]'")
    data.append("    search_button = 'input[value=\"Google Search\"]'")
    data.append(
        "    feeling_lucky_button = "
        "'''input[value=\"I'm Feeling Lucky\"]'''")
    data.append("")
    data.append("")
    data.append("class ResultsPage(object):")
    data.append("    google_logo = 'img[alt=\"Google\"]'")
    data.append("    images_link = 'link=Images'")
    data.append("    search_results = 'div#center_col'")
    data.append("")
    file_path = "%s/%s" % (dir_name_3, "google_objects.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class LoginPage():")
    data.append("")
    data.append("    def login_to_swag_labs(self, sb, username):")
    data.append('        sb.open("https://www.saucedemo.com/")')
    data.append('        sb.type("#user-name", username)')
    data.append('        sb.type("#password", "secret_sauce")')
    data.append("        sb.click('input[type=\"submit\"]')")
    data.append("")
    data.append("")
    data.append("class MyTests(BaseCase):")
    data.append("")
    data.append("    def test_swag_labs_login(self):")
    data.append(
        '        LoginPage().login_to_swag_labs(self, "standard_user")')
    data.append('        self.assert_element("#inventory_container")')
    data.append('        self.assert_text("Products", "div.product_label")')
    data.append("")
    file_path = "%s/%s" % (dir_name_3, "swag_labs_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("class LoginPage():")
    data.append("")
    data.append("    def login_to_swag_labs(self, sb, username):")
    data.append('        sb.open("https://www.saucedemo.com/")')
    data.append('        sb.type("#user-name", username)')
    data.append('        sb.type("#password", "secret_sauce")')
    data.append("        sb.click('input[type=\"submit\"]')")
    data.append("")
    data.append("")
    data.append("class MyTests():")
    data.append("")
    data.append("    def test_swag_labs_login(self, sb):")
    data.append('        LoginPage().login_to_swag_labs(sb, "standard_user")')
    data.append('        sb.assert_element("#inventory_container")')
    data.append('        sb.assert_text("Products", "div.product_label")')
    data.append("")
    file_path = "%s/%s" % (dir_name_3, "sb_swag_test.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    success = (
        '\n' + c1 + '* Directory "' + dir_name + '" was created '
        'with config files and sample tests! *' + cr + '\n')
    print(success)


if __name__ == "__main__":
    invalid_run_command()
