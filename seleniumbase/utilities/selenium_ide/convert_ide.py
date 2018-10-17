"""
Converts a Selenium IDE recording that was exported as a Python WebDriver
unittest file into SeleniumBase Python file.
Works with Katalon Recorder scripts: http://www.katalon.com/automation-recorder

Usage:
        seleniumbase convert [PYTHON_WEBDRIVER_UNITTEST_FILE].py
                (run from anywhere)
    OR
        python convert_ide.py [PYTHON_WEBDRIVER_UNITTEST_FILE].py
                (when run from the "selenium_ide/" folder)
Output:
        [NEW_FILE_SB].py  (adds "_SB" to the original file name)
                          (the original file is kept intact)
"""

import codecs
import re
import sys
from seleniumbase.fixtures import page_utils


def main():
    expected_arg = ("[A PYTHON_WEBDRIVER_UNITTEST_FILE exported from a "
                    "Katalon/Selenium-IDE recording].py")
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1] == "seleniumbase" or (
            sys.argv[0].split('\\')[-1] == "seleniumbase"):
        if num_args < 3 or num_args > 3:
            raise Exception('\n\n* INVALID RUN COMMAND! *  Usage:\n'
                            '"seleniumbase convert %s"\n' % expected_arg)
    else:
        if num_args < 2 or num_args > 2:
            raise Exception('\n\n* INVALID RUN COMMAND! *  Usage:\n'
                            '"python convert_ide.py %s"\n' % expected_arg)
    webdriver_python_file = sys.argv[num_args - 1]
    if not webdriver_python_file.endswith('.py'):
        raise Exception("\n\n`%s` is not a Python file!\n\n"
                        "Expecting: %s\n"
                        % (webdriver_python_file, expected_arg))

    seleniumbase_lines = []
    seleniumbase_lines.append("from seleniumbase import BaseCase")
    seleniumbase_lines.append("")  # Flake8 is very specific on whitespace
    seleniumbase_lines.append("")

    ide_base_url = ""
    in_test_method = False
    has_unicode = False
    uses_keys = False
    uses_select = False

    f = open(webdriver_python_file, 'r')
    all_code = f.read()
    f.close()
    if "def test_" not in all_code:
        raise Exception("\n\n`%s` is not a valid Python unittest.TestCase "
                        "file!\n\nExpecting: %s\n\n"
                        "Did you properly export your Katalon/Selenium-IDE "
                        "recording as a Python WebDriver unittest file?\n"
                        % (webdriver_python_file, expected_arg))
    code_lines = all_code.split('\n')
    for line in code_lines:

        # Handle utf-8 encoding if present
        data = re.findall(r'^\s*# -\*- coding: utf-8 -\*-\s*$', line)
        if data:
            has_unicode = True
            continue

        # Keep SeleniumBase classes if already used in the test script
        data = re.findall(r'^class\s\S+\(BaseCase\):\s*$', line)
        if data:
            seleniumbase_lines.append(line)
            continue

        # Have unittest.TestCase classes inherit BaseCase instead
        data = re.findall(r'^class\s\S+\(unittest\.TestCase\):\s*$', line)
        if data:
            data = data[0].replace("unittest.TestCase", "BaseCase")
            seleniumbase_lines.append(data)
            continue

        # Get base_url if defined
        data = re.match(r'^\s*self.base_url = "(\S+)"\s*$', line)
        if data:
            ide_base_url = data.group(1)
            continue

        # Handle method definitions
        data = re.match(r'^\s*def\s(\S+)\(self[,\s\S]*\):\s*$', line)
        if data:
            method_name = data.group(1)
            if method_name.startswith('test_'):
                in_test_method = True
                seleniumbase_lines.append("")
                seleniumbase_lines.append(data.group())
            else:
                in_test_method = False
            continue

        # If not in a test method, skip
        if not in_test_method:
            continue

        # If a comment, skip
        if line.strip().startswith("#"):
            continue

        # If a blank line, skip
        if len(line.strip()) == 0:
            continue

        # If .clear(), skip because .update_text() already does this
        if line.strip().endswith(".clear()"):
            continue

        # Skip edge case
        data = re.findall(r'^\s*driver = self.driver\s*$', line)
        if data:
            continue

        # Handle page loads
        data = re.match(
            r'^(\s*)driver\.get\((self\.base_url \+ \"/\S*\")\)\s*$', line)
        if data:
            whitespace = data.group(1)
            url = data.group(2)
            url = url.replace("self.base_url", '"%s"' % ide_base_url)
            if '/" + "/' in url:
                url = url.replace('/" + "/', '/')
            if "/' + '/" in url:
                url = url.replace("/' + '/", "/")
            command = '''%sself.open(%s)''' % (whitespace, url)
            seleniumbase_lines.append(command)
            continue

        # Handle more page loads
        data = re.match(
            r'^(\s*)driver\.get\(\"(\S*)\"\)\s*$', line)
        if data:
            whitespace = data.group(1)
            url = data.group(2)
            command = '''%sself.open('%s')''' % (whitespace, url)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_id() + .click()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_id\(\"(\S+)\"\)'''
            r'''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '#%s' % data.group(2)
            selector = selector.replace('[', '\\[').replace(']', '\\]')
            command = '''%sself.click('%s')''' % (whitespace, selector)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_id() + .send_keys()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_id\(\"(\S+)\"\)'''
            r'''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '#%s' % data.group(2)
            selector = selector.replace('[', '\\[').replace(']', '\\]')
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, selector, text)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_id() + .send_keys(Keys.<KEY>)
        data = re.match(
            r'''^(\s*)driver\.find_element_by_id\(\"(\S+)\"\)'''
            r'''\.send_keys\(Keys\.([\S]+)\)\s*$''', line)
        if data:
            uses_keys = True
            whitespace = data.group(1)
            selector = '#%s' % data.group(2)
            selector = selector.replace('[', '\\[').replace(']', '\\]')
            key = 'Keys.%s' % data.group(3)
            command = '''%sself.send_keys('%s', %s)''' % (
                whitespace, selector, key)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_name() + .click()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_name\(\"(\S+)\"\)'''
            r'''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '[name="%s"]' % data.group(2)
            command = '''%sself.click('%s')''' % (whitespace, selector)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_name() + .send_keys()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_name\(\"(\S+)\"\)'''
            r'''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '[name="%s"]' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, selector, text)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_name() + .send_keys(Keys.<KEY>)
        data = re.match(
            r'''^(\s*)driver\.find_element_by_name\(\"(\S+)\"\)'''
            r'''\.send_keys\(Keys\.([\S]+)\)\s*$''', line)
        if data:
            uses_keys = True
            whitespace = data.group(1)
            selector = '[name="%s"]' % data.group(2)
            key = 'Keys.%s' % data.group(3)
            command = '''%sself.send_keys('%s', %s)''' % (
                whitespace, selector, key)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_css_selector() + .click()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_css_selector\(\"([\S\s]+)\"\)'''
            r'''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            command = '''%sself.click('%s')''' % (whitespace, selector)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_css_selector() + .send_keys()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_css_selector\(\"([\S\s]+)\"\)'''
            r'''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, selector, text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_css_selector() + .send_keys(Keys.<KEY>)
        data = re.match(
            r'''^(\s*)driver\.find_element_by_css_selector\(\"([\S\s]+)\"\)'''
            r'''\.send_keys\(Keys\.([\S]+)\)\s*$''', line)
        if data:
            uses_keys = True
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            key = 'Keys.%s' % data.group(3)
            command = '''%sself.send_keys('%s', %s)''' % (
                whitespace, selector, key)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_xpath() + .send_keys()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_xpath\(\"([\S\s]+)\"\)'''
            r'''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text("%s", '%s')''' % (
                whitespace, selector, text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_xpath() + .send_keys(Keys.<KEY>)
        data = re.match(
            r'''^(\s*)driver\.find_element_by_xpath\(\"([\S\s]+)\"\)'''
            r'''\.send_keys\(Keys\.([\S]+)\)\s*$''', line)
        if data:
            uses_keys = True
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            key = 'Keys.%s' % data.group(3)
            command = '''%sself.send_keys("%s", %s)''' % (
                whitespace, selector, key)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle Select / by_css_selector() / select_by_visible_text()
        data = re.match(
            r'''^(\s*)Select\(driver\.find_element_by_css_selector\('''
            r'''\"([\S\s]+)\"\)\)\.select_by_visible_text\('''
            r'''\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            visible_text = '%s' % data.group(3)
            command = '''%sself.pick_select_option_by_text('%s', '%s')''' % (
                whitespace, selector, visible_text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle Select / by_id() / select_by_visible_text()
        data = re.match(
            r'''^(\s*)Select\(driver\.find_element_by_id\('''
            r'''\"([\S\s]+)\"\)\)\.select_by_visible_text\('''
            r'''\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '#%s' % data.group(2)
            visible_text = '%s' % data.group(3)
            command = '''%sself.pick_select_option_by_text('%s', '%s')''' % (
                whitespace, selector, visible_text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle Select / by_xpath() / select_by_visible_text()
        data = re.match(
            r'''^(\s*)Select\(driver\.find_element_by_xpath\('''
            r'''\"([\S\s]+)\"\)\)\.select_by_visible_text\('''
            r'''\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '%s' % data.group(2)
            visible_text = '%s' % data.group(3)
            command = '''%sself.pick_select_option_by_text("%s", '%s')''' % (
                whitespace, selector, visible_text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle Select / by_name() / select_by_visible_text()
        data = re.match(
            r'''^(\s*)Select\(driver\.find_element_by_name\('''
            r'''\"([\S\s]+)\"\)\)\.select_by_visible_text\('''
            r'''\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            selector = '[name="%s"]' % data.group(2)
            visible_text = '%s' % data.group(3)
            command = '''%sself.pick_select_option_by_text('%s', '%s')''' % (
                whitespace, selector, visible_text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_xpath() + .click()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_xpath\(u?\"([\S\s]+)\"\)'''
            r'''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            xpath = '%s' % data.group(2)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%sself.click(%s"%s")''' % (
                whitespace, uni, xpath)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_link_text() + .click()
        data = re.match(
            r'''^(\s*)driver\.find_element_by_link_text\(u?\"([\S\s]+)\"\)'''
            r'''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            link_text = '''%s''' % data.group(2)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%sself.click(%s"link=%s")''' % (
                whitespace, uni, link_text)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.LINK_TEXT, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.LINK_TEXT, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            link_text = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_link_text_present(%s"%s")%s''' % (
                whitespace, pre, uni, link_text, post)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.NAME, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.NAME, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            name = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_element_present('[name="%s"]')%s''' % (
                whitespace, pre, name, post)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.ID, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.ID, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            the_id = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_element_present("#%s")%s''' % (
                whitespace, pre, the_id, post)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.CLASS, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.CLASS, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            the_class = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_element_present(".%s")%s''' % (
                whitespace, pre, the_class, post)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.CSS_SELECTOR, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.CSS_SELECTOR, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            selector = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_element_present("%s")%s''' % (
                whitespace, pre, selector, post)
            seleniumbase_lines.append(command)
            continue

        # Handle self.is_element_present(By.XPATH, *)
        data = re.match(
            r'''^(\s*)([\S\s]*)self\.is_element_present\(By.XPATH, '''
            r'''u?\"([\S\s]+)\"\)([\S\s]*)$''', line)
        if data:
            whitespace = data.group(1)
            pre = data.group(2)
            xpath = '''%s''' % data.group(3)
            post = data.group(4)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%s%sself.is_element_present("%s")%s''' % (
                whitespace, pre, xpath, post)
            seleniumbase_lines.append(command)
            continue

        # Replace "self.base_url" with actual url if not already done
        if 'self.base_url' in line:
            line = line.replace("self.base_url", '"%s"' % ide_base_url)

        # Convert "driver." to "self.driver." if not already done
        if 'driver.' in line and 'self.driver' not in line:
            line = line.replace('driver.', 'self.driver.')

        # Add all other lines to final script without making changes
        seleniumbase_lines.append(line)

    # Chunk processing of inefficient waiting from Selenium IDE
    in_inefficient_wait = False
    whitespace = ""
    lines = seleniumbase_lines
    seleniumbase_lines = []
    for line in lines:
        data = re.match(r'^(\s*)for i in range\(60\):\s*$', line)
        if data:
            in_inefficient_wait = True
            whitespace = data.group(1)
            continue

        data = re.match(r'^(\s*)else: self.fail\("time out"\)\s*$', line)
        if data:
            in_inefficient_wait = False
            continue

        if in_inefficient_wait:
            data = re.match(
                r'''^\s*if self.is_element_present\("([\S\s]+)"\)'''
                r''': break\s*$''', line)
            if data:
                selector = data.group(1)
                command = '%sself.wait_for_element("%s")' % (
                    whitespace, selector)
                seleniumbase_lines.append(command)
                continue

            data = re.match(
                r'''^\s*if self.is_element_present\('([\S\s]+)'\)'''
                r''': break\s*$''', line)
            if data:
                selector = data.group(1)
                command = "%sself.wait_for_element('%s')" % (
                    whitespace, selector)
                seleniumbase_lines.append(command)
                continue

            data = re.match(
                r'''^\s*if self.is_link_text_present'''
                r'''\("([\S\s]+)"\): break\s*$''', line)
            if data:
                uni = ""
                if '(u"' in line:
                    uni = "u"
                link_text = data.group(1)
                command = '''%sself.wait_for_link_text(%s"%s")''' % (
                    whitespace, uni, link_text)
                seleniumbase_lines.append(command)
                continue
        else:
            seleniumbase_lines.append(line)
            continue

    # Is there a Select() still present?
    lines = seleniumbase_lines
    for line_num in range(len(lines)):
        if "Select(self.driver" in lines[line_num]:
            uses_select = True

    # Remove duplicate functionality (wait_for_element)
    lines = seleniumbase_lines
    seleniumbase_lines = []
    num_lines = len(lines)
    for line_num in range(len(lines)):
        data = re.match(
            r'''^\s*self.wait_for_element'''
            r'''\((["|'])([\S\s]+)(["|'])\)'''
            r'''\s*$''', lines[line_num])
        if data:
            # quote_type = data.group(1)
            selector = data.group(2)
            selector = re.escape(selector)
            selector = page_utils.escape_quotes_if_needed(selector)
            if int(line_num) < num_lines - 1:
                regex_string = (r'''^\s*self.click\(["|']''' +
                                selector + r'''["|']\)\s*$''')
                data2 = re.match(regex_string, lines[line_num + 1])
                if data2:
                    continue
                regex_string = (r'''^\s*self.update_text\(["|']''' +
                                selector +
                                r'''["|'], [\S\s]+\)\s*$''')
                data2 = re.match(regex_string, lines[line_num + 1])
                if data2:
                    continue
        seleniumbase_lines.append(lines[line_num])

    # Remove duplicate functionality (wait_for_link_text)
    lines = seleniumbase_lines
    seleniumbase_lines = []
    num_lines = len(lines)
    for line_num in range(len(lines)):
        data = re.match(
            r'''^\s*self.wait_for_link_text'''
            r'''\((["|'])([\S\s]+)(["|'])\)'''
            r'''\s*$''', lines[line_num])
        if data:
            # quote_type = data.group(1)
            link_text = data.group(2)
            link_text = re.escape(link_text)
            link_text = page_utils.escape_quotes_if_needed(link_text)
            if int(line_num) < num_lines - 2:
                regex_string = (r'''^\s*self.click\(["|']link=''' +
                                link_text + r'''["|']\)\s*$''')
                data2 = re.match(regex_string, lines[line_num + 1])
                if data2:
                    continue
        seleniumbase_lines.append(lines[line_num])

    seleniumbase_code = ""
    if has_unicode:
        seleniumbase_code = "# -*- coding: utf-8 -*-\n"
    if uses_keys:
        seleniumbase_code += (
            "from selenium.webdriver.common.keys import Keys\n")
    if uses_select:
        seleniumbase_code += (
            "from selenium.webdriver.support.ui import Select\n")
    for line in seleniumbase_lines:
        seleniumbase_code += line
        seleniumbase_code += "\n"
    # print(seleniumbase_code)  # (For debugging)

    # Create SeleniumBase test file
    base_file_name = webdriver_python_file.split('.py')[0]
    converted_file_name = base_file_name + "_SB.py"
    out_file = codecs.open(converted_file_name, "w+")
    out_file.writelines(seleniumbase_code)
    out_file.close()
    print('\n>>> [%s] was created from [%s]\n' % (
        converted_file_name, webdriver_python_file))


if __name__ == "__main__":
    main()
