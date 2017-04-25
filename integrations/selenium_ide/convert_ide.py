"""
Converts a Selenium IDE WebDriver-exported test file into a SeleniumBase file

Usage:
python convert_ide.py [MY_TEST.py]
Output:
[MY_TEST_SB.py]  (Adds "_SB" to the file name)
"""

import codecs
import re
import sys


def main():
    expected_arg = "[A Selenium IDE recording exported to Python WebDriver]"
    num_args = len(sys.argv)
    if num_args < 2 or num_args > 2:
        raise Exception("\n* INVALID RUN COMMAND! *  Usage:\n"
                        "python convert_ide.py %s\n" % expected_arg)
    elif num_args == 2:
        if not sys.argv[1].endswith('.py'):
            raise Exception("Not a Python file!")
    webdriver_python_file = sys.argv[1]

    seleniumbase_lines = []
    seleniumbase_lines.append("from seleniumbase import BaseCase")
    seleniumbase_lines.append("")  # Flake8 is very specific on whitespace
    seleniumbase_lines.append("")

    ide_base_url = ""
    in_test_method = False
    has_unicode = False

    f = open(webdriver_python_file, 'r')
    all_code = f.read()
    f.close()
    if "def test_" not in all_code:
        raise Exception("Not a valid Python test file!")
    code_lines = all_code.split('\n')
    for line in code_lines:

        # Handle utf-8 encoding if present
        data = re.findall('^\s*# -\*- coding: utf-8 -\*-\s*$', line)
        if data:
            has_unicode = True
            continue

        # Handle class definition
        data = re.findall('^class\s\S+\(unittest\.TestCase\):\s*$', line)
        if data:
            data = data[0].replace("unittest.TestCase", "BaseCase")
            seleniumbase_lines.append(data)
            continue

        # Get base_url if defined
        data = re.match('^\s*self.base_url = "(\S+)"\s*$', line)
        if data:
            ide_base_url = data.group(1)
            continue

        # Handle method definitions
        data = re.match('^\s*def\s(\S+)\(self[,\s\S]*\):\s*$', line)
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
        data = re.findall('^\s*driver = self.driver\s*$', line)
        if data:
            continue

        # Handle page loads
        data = re.match(
            '^(\s*)driver\.get\((self\.base_url \+ \"/\S*\")\)\s*$', line)
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
            '^(\s*)driver\.get\(\"(\S*)\"\)\s*$', line)
        if data:
            whitespace = data.group(1)
            url = data.group(2)
            command = '''%sself.open('%s')''' % (whitespace, url)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_id() + .click()
        data = re.match(
            '''^(\s*)driver\.find_element_by_id\(\"(\S+)\"\)'''
            '''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '#%s' % data.group(2)
            command = '''%sself.click('%s')''' % (whitespace, css_selector)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_id() + .send_keys()
        data = re.match(
            '''^(\s*)driver\.find_element_by_id\(\"(\S+)\"\)'''
            '''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '#%s' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, css_selector, text)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_name() + .click()
        data = re.match(
            '''^(\s*)driver\.find_element_by_name\(\"(\S+)\"\)'''
            '''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '[name="%s"]' % data.group(2)
            command = '''%sself.click('%s')''' % (whitespace, css_selector)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_name() + .send_keys()
        data = re.match(
            '''^(\s*)driver\.find_element_by_name\(\"(\S+)\"\)'''
            '''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '[name="%s"]' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, css_selector, text)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_css_selector() + .click()
        data = re.match(
            '''^(\s*)driver\.find_element_by_css_selector\(\"([\S\s]+)\"\)'''
            '''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '%s' % data.group(2)
            command = '''%sself.click('%s')''' % (whitespace, css_selector)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_css_selector() + .send_keys()
        data = re.match(
            '''^(\s*)driver\.find_element_by_css_selector\(\"([\S\s]+)\"\)'''
            '''\.send_keys\(\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '%s' % data.group(2)
            text = data.group(3)
            command = '''%sself.update_text('%s', '%s')''' % (
                whitespace, css_selector, text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle Select / by_css_selector() / select_by_visible_text()
        data = re.match(
            '''^(\s*)Select\(driver\.find_element_by_css_selector\('''
            '''\"([\S\s]+)\"\)\)\.select_by_visible_text\('''
            '''\"([\S\s]+)\"\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            css_selector = '%s' % data.group(2)
            visible_text = '%s' % data.group(3)
            command = '''%sself.pick_select_option_by_text('%s', '%s')''' % (
                whitespace, css_selector, visible_text)
            if command.count('\\"') == command.count('"'):
                command = command.replace('\\"', '"')
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_xpath() + .click()
        data = re.match(
            '''^(\s*)driver\.find_element_by_xpath\(u?\"([\S\s]+)\"\)'''
            '''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            xpath = '%s' % data.group(2)
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%sself.click_xpath(%s"%s")''' % (
                whitespace, uni, xpath)
            seleniumbase_lines.append(command)
            continue

        # Handle .find_element_by_link_text() + .click()
        data = re.match(
            '''^(\s*)driver\.find_element_by_link_text\(u?\"([\S\s]+)\"\)'''
            '''\.click\(\)\s*$''', line)
        if data:
            whitespace = data.group(1)
            link_text = '''%s''' % data.group(2)
            uni = ""
            if '(u"' in line:
                uni = "u"
                has_unicode = True
            command = '''%sself.click_link_text(%s"%s")''' % (
                whitespace, uni, link_text)
            seleniumbase_lines.append(command)
            continue

        # Replace "self.base_url" with actual url if not already done
        if 'self.base_url' in line:
            line = line.replace("self.base_url", '"%s"' % ide_base_url)

        # Convert driver. to self.driver. if not already done
        if 'driver.' in line and 'self.driver' not in line:
            line = line.replace('driver.', 'self.driver.')

        # Add all other lines to final script without making changes
        seleniumbase_lines.append(line)

    seleniumbase_code = ""
    if has_unicode:
        seleniumbase_code = "# -*- coding: utf-8 -*-\n"
    for line in seleniumbase_lines:
        seleniumbase_code += line
        seleniumbase_code += "\n"
    # print seleniumbase_code  # (For debugging)

    # Create SeleniumBase test file
    base_file_name = webdriver_python_file.split('.py')[0]
    converted_file_name = base_file_name + "_SB.py"
    out_file = codecs.open(converted_file_name, "w+")
    out_file.writelines(seleniumbase_code)
    out_file.close()
    print("%s successfully created from %s\n" % (
        converted_file_name, webdriver_python_file))


if __name__ == "__main__":
    main()
