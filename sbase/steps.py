from behave import step


def normalize_text(text):
    text = text.replace("\\\\", "\\").replace("\\t", "\t").replace("\\n", "\n")
    text = text.replace('\\"', '"').replace("\\'", "'")
    return text


@step("Open '{url}'")
@step('Open "{url}"')
@step("Open URL '{url}'")
@step('Open URL "{url}"')
def open_url(context, url):
    sb = context.sb
    sb.open(url)


@step("Click '{selector}'")
@step('Click "{selector}"')
@step("Click element '{selector}'")
@step('Click element "{selector}"')
def click_element(context, selector):
    sb = context.sb
    sb.click(selector)


@step("Type text '{text}' into '{selector}'")
@step('Type text "{text}" into "{selector}"')
@step("Type text '{text}' into \"{selector}\"")
@step('Type text "{text}" into \'{selector}\'')
@step("Type '{text}' into '{selector}'")
@step('Type "{text}" into "{selector}"')
@step("Type '{text}' into \"{selector}\"")
@step('Type "{text}" into \'{selector}\'')
@step("Into '{selector}' type '{text}'")
@step('Into "{selector}" type "{text}"')
@step("Into '{selector}' type \"{text}\"")
@step('Into "{selector}" type \'{text}\'')
def type_text(context, selector, text):
    sb = context.sb
    text = normalize_text(text)
    sb.type(selector, text)


@step("Add text '{text}' into '{selector}'")
@step('Add text "{text}" into "{selector}"')
@step("Add text '{text}' into \"{selector}\"")
@step('Add text "{text}" into \'{selector}\'')
@step("Into '{selector}' add '{text}'")
@step('Into "{selector}" add "{text}"')
@step("Into '{selector}' add \"{text}\"")
@step('Into "{selector}" add \'{text}\'')
def add_text(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.add_text(selector, text)


@step("Assert element '{selector}'")
@step('Assert element "{selector}"')
def assert_element(context, selector):
    sb = context.sb
    sb.assert_element(selector)


@step("Assert text '{text}' in '{selector}'")
@step('Assert text "{text}" in "{selector}"')
@step("Assert text '{text}' in \"{selector}\"")
@step('Assert text "{text}" in \'{selector}\'')
def assert_text_in_element(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_text(text, selector)


@step("Assert text '{text}'")
@step('Assert text "{text}"')
def assert_text(context, text):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_text(text)


@step("Assert exact text '{text}' in '{selector}'")
@step('Assert exact text "{text}" in "{selector}"')
@step("Assert exact text '{text}' in \"{selector}\"")
@step('Assert exact text "{text}" in \'{selector}\'')
def assert_exact_text(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_exact_text(text, selector)


@step("Highlight '{selector}'")
@step('Highlight "{selector}"')
@step("Highlight element '{selector}'")
@step('Highlight element "{selector}"')
def highlight_element(context, selector):
    sb = context.sb
    sb.highlight(selector)


@step("Click link '{link}'")
@step('Click link "{link}"')
def click_link(context, link):
    sb = context.sb
    sb.click_link(link)


@step("JS click '{selector}'")
@step('JS click "{selector}"')
@step("JS click element '{selector}'")
@step('JS click element "{selector}"')
def js_click(context, selector):
    sb = context.sb
    sb.js_click(selector)


@step("Save screenshot to logs")
@step("Save a screenshot to the logs")
def save_screenshot_to_logs(context):
    sb = context.sb
    sb.save_screenshot_to_logs()


@step("Refresh page")
def refresh_page(context):
    sb = context.sb
    sb.refresh_page()


@step("Go back")
def go_back(context):
    sb = context.sb
    sb.go_back()


@step("Go forward")
def go_forward(context):
    sb = context.sb
    sb.go_forward()


@step("JS type '{text}' into '{selector}'")
@step('JS type "{text}" into "{selector}"')
@step("JS type '{text}' into \"{selector}\"")
@step('JS type "{text}" into \'{selector}\'')
@step("JS type text '{text}' into '{selector}'")
@step('JS type text "{text}" into "{selector}"')
@step("JS type text '{text}' into \"{selector}\"")
@step('JS type text "{text}" into \'{selector}\'')
def js_type(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.js_type(selector, text)


@step("Set value of '{selector}' to '{text}'")
@step('Set value of "{selector}" to "{text}"')
@step("Set value of \"{selector}\" to '{text}'")
@step('Set value of \'{selector}\' to "{text}"')
def set_value(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.set_value(selector, text)


@step("Switch to iframe '{frame}'")
@step('Switch to iframe "{frame}"')
@step("Switch to frame '{frame}'")
@step('Switch to frame "{frame}"')
def switch_to_frame(context, frame):
    sb = context.sb
    sb.switch_to_frame(frame)


@step("Switch to default content")
@step("Exit from iframes")
@step("Exit from frames")
def switch_to_default_content(context):
    sb = context.sb
    sb.switch_to_default_content()


@step("Switch to parent frame")
@step("Exit current iframe")
@step("Exit current frame")
def switch_to_parent_frame(context):
    sb = context.sb
    sb.switch_to_parent_frame()


@step("Into '{selector}' enter MFA code '{totp_key}'")
@step('Into "{selector}" enter MFA code "{totp_key}"')
@step("Into '{selector}' enter MFA code \"{totp_key}\"")
@step('Into "{selector}" enter MFA code \'{totp_key}\'')
@step("Into '{selector}' do MFA '{totp_key}'")
@step('Into "{selector}" do MFA "{totp_key}"')
@step("Into '{selector}' do MFA \"{totp_key}\"")
@step('Into "{selector}" do MFA \'{totp_key}\'')
@step("Enter MFA code '{totp_key}' into '{selector}'")
@step('Enter MFA code "{totp_key}" into "{selector}"')
@step("Enter MFA code \"{totp_key}\" into '{selector}'")
@step('Enter MFA code \'{totp_key}\' into "{selector}"')
@step("Do MFA '{totp_key}' into '{selector}'")
@step('Do MFA "{totp_key}" into "{selector}"')
@step("Do MFA \"{totp_key}\" into '{selector}'")
@step('Do MFA \'{totp_key}\' into "{selector}"')
def enter_mfa_code(context, selector, totp_key):
    sb = context.sb
    sb.enter_mfa_code(selector, totp_key)


@step("Open if not '{url}'")
@step('Open if not "{url}"')
@step("Open if not URL '{url}'")
@step('Open if not URL "{url}"')
def open_if_not_url(context, url):
    sb = context.sb
    sb.open_if_not_url(url)


@step("Select if unselected '{selector}'")
@step('Select if unselected "{selector}"')
def select_if_unselected(context, selector):
    sb = context.sb
    sb.select_if_unselected(selector)


@step("Unselect if selected '{selector}'")
@step('Unselect if selected "{selector}"')
def unselect_if_selected(context, selector):
    sb = context.sb
    sb.unselect_if_selected(selector)


@step("Check if unchecked '{selector}'")
@step('Check if unchecked "{selector}"')
def check_if_unchecked(context, selector):
    sb = context.sb
    sb.check_if_unchecked(selector)


@step("Uncheck if checked '{selector}'")
@step('Uncheck if checked "{selector}"')
def uncheck_if_checked(context, selector):
    sb = context.sb
    sb.uncheck_if_checked(selector)


@step("Drag '{drag_selector}' into '{drop_selector}'")
@step('Drag "{drag_selector}" into "{drop_selector}"')
@step("Drag '{drag_selector}' into \"{drop_selector}\"")
@step('Drag "{drag_selector}" into \'{drop_selector}\'')
def drag_and_drop(context, drag_selector, drop_selector):
    sb = context.sb
    sb.drag_and_drop(drag_selector, drop_selector)


@step("Hover '{hover_selector}' and click '{click_selector}'")
@step('Hover "{hover_selector}" and click "{click_selector}"')
@step("Hover '{hover_selector}' and click \"{click_selector}\"")
@step('Hover "{hover_selector}" and click \'{click_selector}\'')
def hover_and_click(context, hover_selector, click_selector):
    sb = context.sb
    sb.hover_and_click(hover_selector, click_selector)


@step("Find '{selector}' and select '{text}'")
@step('Find "{selector}" and select "{text}"')
@step("Find '{selector}' and select \"{text}\"")
@step('Find "{selector}" and select \'{text}\'')
def select_option_by_text(context, selector, text):
    sb = context.sb
    text = normalize_text(text)
    sb.select_option_by_text(selector, text)


@step("Find '{selector}' and select '{text}' by {option}")
@step('Find "{selector}" and select "{text}" by {option}')
@step("Find '{selector}' and select \"{text}\" by {option}")
@step('Find "{selector}" and select \'{text}\' by {option}')
def select_option_by_option(context, selector, text, option):
    sb = context.sb
    text = normalize_text(text)
    if option.startswith("'") or option.startswith('"'):
        option = option[1:]
    if option.endswith("'") or option.endswith('"'):
        option = option[:-1]
    if option == "text":
        sb.select_option_by_text(selector, text)
    elif option == "index":
        sb.select_option_by_index(selector, text)
    elif option == "value":
        sb.select_option_by_value(selector, text)
    else:
        raise Exception("Unknown option: %s" % option)


@step("Wait for '{selector}'")
@step('Wait for "{selector}"')
@step("Wait for element '{selector}'")
@step('Wait for element "{selector}"')
def wait_for_element(context, selector):
    sb = context.sb
    sb.wait_for_element(selector)


@step("Double click '{selector}'")
@step('Double click "{selector}"')
@step("Double click element '{selector}'")
@step('Double click element "{selector}"')
def double_click_element(context, selector):
    sb = context.sb
    sb.double_click(selector)


@step("Slow click '{selector}'")
@step('Slow click "{selector}"')
@step("Slow click element '{selector}'")
@step('Slow click element "{selector}"')
def slow_click_element(context, selector):
    sb = context.sb
    sb.slow_click(selector)


@step("Clear text field '{selector}'")
@step('Clear text field "{selector}"')
def clear_text_field(context, selector):
    sb = context.sb
    sb.clear(selector)


@step("Maximize window")
def maximize_window(context):
    sb = context.sb
    sb.maximize_window()


@step("Get new driver")
def get_new_driver(context):
    sb = context.sb
    sb.get_new_driver()


@step("Switch to default driver")
def switch_to_default_driver(context):
    sb = context.sb
    sb.switch_to_default_driver()


@step("Press up arrow")
def press_up_arrow(context):
    sb = context.sb
    sb.press_up_arrow()


@step("Press down arrow")
def press_down_arrow(context):
    sb = context.sb
    sb.press_down_arrow()


@step("Press left arrow")
def press_left_arrow(context):
    sb = context.sb
    sb.press_left_arrow()


@step("Press right arrow")
def press_right_arrow(context):
    sb = context.sb
    sb.press_right_arrow()


@step("Clear all cookies")
@step("Delete all cookies")
def delete_all_cookies(context):
    sb = context.sb
    sb.delete_all_cookies()


@step("Clear Local Storage")
@step("Delete Local Storage")
def clear_local_storage(context):
    sb = context.sb
    sb.clear_local_storage()


@step("Clear Session Storage")
@step("Delete Session Storage")
def clear_session_storage(context):
    sb = context.sb
    sb.clear_session_storage()


@step("JS click all '{selector}'")
@step('JS click all "{selector}"')
def js_click_all(context, selector):
    sb = context.sb
    sb.js_click_all(selector)


@step("Click '{selector}' at ({px},{py})")
@step('Click "{selector}" at ({px},{py})')
@step("Click '{selector}' at ({px}, {py})")
@step('Click "{selector}" at ({px}, {py})')
def click_with_offset(context, selector, px, py):
    sb = context.sb
    sb.click_with_offset(selector, px, py)


@step("Into '{selector}' choose file '{file_path}'")
@step('Into "{selector}" choose file "{file_path}"')
@step("Into '{selector}' choose file \"{file_path}\"")
@step('Into "{selector}" choose file \'{file_path}\'')
def choose_file(context, selector, file_path):
    sb = context.sb
    sb.choose_file(selector, file_path)


@step("Set content to frame '{frame}'")
@step('Set content to frame "{frame}"')
def set_content_to_frame(context, frame):
    sb = context.sb
    sb.set_content_to_frame(frame)


@step("Set content to default")
def set_content_to_default(context):
    sb = context.sb
    sb.set_content_to_default()


@step("Set content to parent")
def set_content_to_parent(context):
    sb = context.sb
    sb.set_content_to_parent()


@step("Assert element present '{selector}'")
@step('Assert element present "{selector}"')
def assert_element_present(context, selector):
    sb = context.sb
    sb.assert_element_present(selector)


@step("Assert element not visible '{selector}'")
@step('Assert element not visible "{selector}"')
def assert_element_not_visible(context, selector):
    sb = context.sb
    sb.assert_element_not_visible(selector)


@step("Assert link text '{text}'")
@step('Assert link text "{text}"')
def assert_link_text(context, text):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_link_text(text)


@step("Assert title '{title}'")
@step('Assert title "{title}"')
def assert_title(context, title):
    sb = context.sb
    title = normalize_text(title)
    sb.assert_title(title)


@step("Assert downloaded file '{file}'")
@step('Assert downloaded file "{file}"')
def assert_downloaded_file(context, file):
    sb = context.sb
    sb.assert_downloaded_file(file)


@step("Download '{file}' to downloads")
@step('Download "{file}" to downloads')
@step("Download file '{file}' to downloads")
@step('Download file "{file}" to downloads')
def download_file(context, file):
    sb = context.sb
    sb.download_file(file)


@step("Download '{file}' to '{destination}'")
@step('Download "{file}" to "{destination}"')
@step("Download file '{file}' to '{destination}'")
@step('Download file "{file}" to "{destination}"')
def download_file_to_destination(context, file, destination):
    sb = context.sb
    sb.download_file(file, destination)


@step("In '{selector}' assert attribute \'{attribute}\'")
@step('In "{selector}" assert attribute \"{attribute}\"')
@step("In \"{selector}\" assert attribute '{attribute}'")
@step('In \'{selector}\' assert attribute "{attribute}"')
def assert_attribute(context, selector, attribute):
    sb = context.sb
    sb.assert_attribute(selector, attribute)


@step("In '{selector}' assert attribute/value '{attribute}'/'{value}'")
@step('In "{selector}" assert attribute/value "{attribute}"/"{value}"')
@step("In \"{selector}\" assert attribute/value '{attribute}'/\"{value}\"")
@step('In \'{selector}\' assert attribute/value "{attribute}"/\'{value}\'')
@step("In '{selector}' assert attribute/value '{attribute}'/\"{value}\"")
@step('In "{selector}" assert attribute/value "{attribute}"/\'{value}\'')
@step("In \"{selector}\" assert attribute/value '{attribute}'/'{value}'")
@step('In \'{selector}\' assert attribute/value "{attribute}"/"{value}"')
def assert_attribute_has_value(context, selector, attribute, value):
    sb = context.sb
    value = normalize_text(value)
    sb.assert_attribute(selector, attribute, value)


@step("Show file choosers")
@step("Show hidden file choosers")
def show_file_choosers(context):
    sb = context.sb
    sb.show_file_choosers()


@step("Sleep for {seconds} seconds")
def sleep(context, seconds):
    sb = context.sb
    sb.sleep(float(seconds))


@step("Activate Demo Mode")
def activate_demo_mode(context):
    sb = context.sb
    sb.activate_demo_mode()


@step("Deactivate Demo Mode")
def deactivate_demo_mode(context):
    sb = context.sb
    sb.deactivate_demo_mode()


@step("Deferred assert element '{selector}'")
@step('Deferred assert element "{selector}"')
def deferred_assert_element(context, selector):
    sb = context.sb
    sb.deferred_assert_element(selector)


@step("Deferred assert element present '{selector}'")
@step('Deferred assert element present "{selector}"')
def deferred_assert_element_present(context, selector):
    sb = context.sb
    sb.deferred_assert_element_present(selector)


@step("Deferred assert text '{text}' in '{selector}'")
@step('Deferred assert text "{text}" in "{selector}"')
@step("Deferred assert text '{text}' in \"{selector}\"")
@step('Deferred assert text "{text}" in \'{selector}\'')
def deferred_assert_text_in_element(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.deferred_assert_text(text, selector)


@step("Deferred assert text '{text}'")
@step('Deferred assert text "{text}"')
def deferred_assert_text(context, text):
    sb = context.sb
    text = normalize_text(text)
    sb.deferred_assert_text(text)


@step("Deferred assert exact text '{text}' in '{selector}'")
@step('Deferred assert exact text "{text}" in "{selector}"')
def deferred_assert_exact_text(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.deferred_assert_exact_text(text, selector)


@step("Process deferred asserts")
def process_deferred_asserts(context):
    sb = context.sb
    sb.process_deferred_asserts()


@step("Assert text not visible '{text}' in '{selector}'")
@step('Assert text not visible "{text}" in "{selector}"')
@step("Assert text not visible '{text}' in \"{selector}\"")
@step('Assert text not visible "{text}" in \'{selector}\'')
def assert_text_not_visible_in_element(context, text, selector):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_text_not_visible(text, selector)


@step("Assert text not visible '{text}'")
@step('Assert text not visible "{text}"')
def assert_text_not_visible(context, text):
    sb = context.sb
    text = normalize_text(text)
    sb.assert_text_not_visible(text)
