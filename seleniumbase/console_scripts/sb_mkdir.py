"""
Creates a new folder for running SeleniumBase scripts.

Usage:
seleniumbase mkdir [DIRECTORY_NAME]
Output:
Creates a new folder for running SeleniumBase scripts.
The new folder contains default config files,
sample tests for helping new users get started, and
Python boilerplates for setting up customized
test frameworks.
"""

import codecs
import os
import sys


def invalid_run_command():
    exp = ("  ** mkdir **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase mkdir [DIRECTORY_NAME]\n"
    exp += "  Example:\n"
    exp += "          seleniumbase mkdir browser_tests\n"
    exp += "  Output:\n"
    exp += "          Creates a new folder for running SeleniumBase scripts.\n"
    exp += "          The new folder contains default config files,\n"
    exp += "          sample tests for helping new users get started, and\n"
    exp += "          Python boilerplates for setting up customized\n"
    exp += "          test frameworks.\n"
    print("")
    raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)


def main():
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1] == "seleniumbase" or (
            sys.argv[0].split('\\')[-1] == "seleniumbase"):
        if num_args < 3 or num_args > 3:
            invalid_run_command()
    else:
        invalid_run_command()
    dir_name = sys.argv[num_args - 1]
    if len(str(dir_name)) < 2:
        raise Exception('Directory name length must be at least 2 '
                        'characters long!')
    if os.path.exists(os.getcwd() + '/' + dir_name):
        raise Exception('Directory "%s" already exists '
                        'in the current path!\n' % dir_name)
    else:
        os.mkdir(dir_name)

        data = []
        data.append("[pytest]")
        data.append("addopts = --capture=no --ignore conftest.py")
        data.append("filterwarnings = ignore::DeprecationWarning")
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
        file_path = "%s/%s" % (dir_name, "config.cfg")
        file = codecs.open(file_path, "w+", "utf-8")
        file.writelines("\r\n".join(data))
        file.close()

        data = []
        data.append("from seleniumbase import BaseCase")
        data.append("")
        data.append("")
        data.append("class MyTestClass(BaseCase):")
        data.append("")
        data.append("    def test_basic(self):")
        data.append("        self.open('http://xkcd.com/353/')")
        data.append("        self.assert_element('img[alt=\"Python\"]')")
        data.append("        self.click('a[rel=\"license\"]')")
        data.append("        self.assert_text('free to copy', 'div center')")
        data.append("        self.open(\"http://xkcd.com/1481/\")")
        data.append(
            "        title = self.get_attribute(\"#comic img\", \"title\")")
        data.append(
            "        self.assertTrue(\"86,400 seconds per day\" in title)")
        data.append("        self.click('link=Blag')")
        data.append(
            "        self.assert_text('The blag of the webcomic', 'h2')")
        data.append("        self.update_text('input#s', 'Robots!\\n')")
        data.append("        self.assert_text('Hooray robots!', '#content')")
        data.append("        self.open('http://xkcd.com/1319/')")
        data.append("        self.assert_text('Automation', 'div#ctitle')")
        data.append("")
        file_path = "%s/%s" % (dir_name, "my_first_test.py")
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
        data.append("        super(BaseTestCase, self).setUp()")
        data.append("        # Add custom setUp code AFTER the super() line")
        data.append("")
        data.append("    def tearDown(self):")
        data.append("        # Add custom code BEFORE the super() line")
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
        data.append("    html = 'html'")
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
        data.append("from .bing_objects import Page")
        data.append("")
        data.append("")
        data.append("class BingTests(BaseCase):")
        data.append("")
        data.append("    def test_bing(self):")
        data.append("        self.open('https://bing.com')")
        data.append("        self.assert_text('Bing', Page.logo_box)")
        data.append("        self.update_text(Page.search_box, 'github')")
        data.append("        self.assert_element('li[query=\"github\"]')")
        data.append("        self.click(Page.search_button)")
        data.append(
            "        self.assert_text('github.com', Page.search_results)")
        data.append("        self.click_link_text('Images')")
        data.append("        self.assert_element('img[alt*=\"github\"]')")
        data.append("")
        file_path = "%s/%s" % (dir_name_3, "bing_test.py")
        file = codecs.open(file_path, "w+", "utf-8")
        file.writelines("\r\n".join(data))
        file.close()

        data = []
        data.append("class Page(object):")
        data.append("    logo_box = '#sbox div[class*=logo]'")
        data.append("    search_box = 'input.b_searchbox'")
        data.append("    search_button = 'input[name=\"go\"]'")
        data.append("    search_results = '#b_results'")
        data.append("")
        file_path = "%s/%s" % (dir_name_3, "bing_objects.py")
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
        data.append("        self.open('https://google.com')")
        data.append(
            "        self.update_text(HomePage.search_box, 'github')")
        data.append("        self.assert_element(HomePage.list_box)")
        data.append("        self.assert_element(HomePage.search_button)")
        data.append(
            "        self.assert_element(HomePage.feeling_lucky_button)")
        data.append("        self.click(HomePage.search_button)")
        data.append(
            "        self.assert_text('github.com', "
            "ResultsPage.search_results)")
        data.append("        self.click_link_text('Images')")
        data.append("        source = self.get_page_source()")
        data.append(
            "        self.assertTrue('Image result for github' in source)")
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
        data.append("    search_results = 'div#center_col'")
        data.append("")
        file_path = "%s/%s" % (dir_name_3, "google_objects.py")
        file = codecs.open(file_path, "w+", "utf-8")
        file.writelines("\r\n".join(data))
        file.close()
        print('''\n* Directory "%s" was created with config files '''
              '''and sample tests! *\n''' % dir_name)


if __name__ == "__main__":
    main()
