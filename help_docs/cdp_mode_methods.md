<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> SeleniumBase CDP Mode Methods (CDP Mode API Reference)</h2>

Here's a list of SeleniumBase CDP Mode method definitions, which are defined in **[sb_cdp.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/sb_cdp.py)**

### 🐙 <b translate="no">CDP Mode</b> API / Methods

```python
sb.get(url, **kwargs)
sb.open(url, **kwargs)  # Same as sb.get(url, **kwargs) in CDP Mode
sb.goto(url, **kwargs)  # Same as sb.get(url, **kwargs) in CDP Mode
sb.reload(ignore_cache=True, script_to_evaluate_on_load=None)
sb.refresh(*args, **kwargs)
sb.get_event_loop()
sb.get_rd_host()  # Returns the remote-debugging host
sb.get_rd_port()  # Returns the remote-debugging port
sb.get_rd_url()  # Returns the remote-debugging URL
sb.get_endpoint_url()  # Same as sb.get_rd_url()
sb.get_port()  # Same as sb.get_rd_port()
sb.get_websocket_url()  # Returns the websocket URL
sb.add_handler(event, handler)
sb.find_element(selector, best_match=False, timeout=None)
sb.find(selector, best_match=False, timeout=None)
sb.locator(selector, best_match=False, timeout=None)
sb.find_element_by_text(text, tag_name=None, timeout=None)
sb.find_all(selector, timeout=None)
sb.find_elements_by_text(text, tag_name=None)
sb.select(selector, timeout=None)
sb.select_all(selector, timeout=None)
sb.find_elements(selector, timeout=None)
sb.find_visible_elements(selector, timeout=None)
sb.click(selector, timeout=None, scroll=True)
sb.click_if_visible(selector, timeout=0, scroll=True)
sb.click_visible_elements(selector, limit=0, scroll=True)
sb.click_nth_element(selector, number, scroll=True)
sb.click_nth_visible_element(selector, number, scroll=True)
sb.click_with_offset(selector, x, y, center=False, scroll=True)
sb.click_link(link_text)
sb.go_back()
sb.go_forward()
sb.get_navigation_history()
sb.tile_windows(windows=None, max_columns=0)
sb.grant_permissions(permissions, origin=None)
sb.grant_all_permissions()
sb.reset_permissions()
sb.get_all_urls(absolute=True)
sb.get_all_cookies(*args, **kwargs)
sb.set_all_cookies(*args, **kwargs)
sb.save_cookies(*args, **kwargs)
sb.load_cookies(*args, **kwargs)
sb.clear_cookies()
sb.sleep(seconds)
sb.bring_active_window_to_front()
sb.bring_to_front()
sb.get_active_element()
sb.get_active_element_css()
sb.click_active_element()
sb.mouse_click(selector, timeout=None, scroll=True)
sb.nested_click(parent_selector, selector)
sb.get_nested_element(parent_selector, selector)
sb.select_option_by_text(dropdown_selector, option)
sb.select_option_by_index(dropdown_selector, option)
sb.select_option_by_value(dropdown_selector, option)
sb.flash(selector, duration=1, color="44CC88", pause=0)
sb.highlight(selector)
sb.focus(selector)
sb.highlight_overlay(selector)
sb.get_parent(element)
sb.remove_element(selector)
sb.remove_from_dom(selector)
sb.remove_elements(selector)
sb.send_keys(selector, text, timeout=None)
sb.press_keys(selector, text, timeout=None)
sb.type(selector, text, timeout=None)
sb.set_value(selector, text, timeout=None)
sb.clear_input(selector, timeout=None)
sb.clear(selector, timeout=None)
sb.submit(selector)
sb.evaluate(expression)
sb.execute_script(expression)
sb.js_dumps(obj_name)
sb.maximize()
sb.minimize()
sb.medimize()
sb.set_window_rect(x, y, width, height)
sb.reset_window_size()
sb.open_new_window(url=None, switch_to=True)
sb.switch_to_window(window)
sb.switch_to_newest_window()
sb.open_new_tab(url=None, switch_to=True)
sb.switch_to_tab(tab)
sb.switch_to_newest_tab()
sb.close_active_tab()
sb.get_active_tab()
sb.get_tabs()
sb.get_window()
sb.get_text(selector="body")
sb.get_title()
sb.get_current_url()
sb.get_origin()
sb.get_html(include_shadow_dom=True)
sb.get_page_source(include_shadow_dom=True)
sb.get_beautiful_soup(source=None)
sb.get_user_agent()
sb.get_cookie_string()
sb.get_locale_code()
sb.get_local_storage_item(key)
sb.get_session_storage_item(key)
sb.get_screen_rect()
sb.get_window_rect()
sb.get_window_size()
sb.get_window_position()
sb.get_element_rect(selector, timeout=None)
sb.get_element_size(selector, timeout=None)
sb.get_element_position(selector, timeout=None)
sb.get_gui_element_rect(selector, timeout=None)
sb.get_gui_element_center(selector, timeout=None)
sb.get_document()
sb.get_flattened_document()
sb.get_element_attributes(selector)
sb.get_element_attribute(selector, attribute)
sb.get_attribute(selector, attribute)
sb.get_element_html(selector)
sb.get_mfa_code(totp_key=None)
sb.enter_mfa_code(selector, totp_key=None, timeout=None)
sb.activate_messenger()
sb.set_messenger_theme(theme="default", location="default")
sb.post_message(message, duration=None, pause=True, style="info")
sb.download_file(file_url)
sb.save_file_as(file_url, new_file_name)
sb.assert_downloaded_file(file, timeout=None)
sb.get_path_of_downloaded_file(file)
sb.set_download_path(path)
sb.set_locale(locale)
sb.set_local_storage_item(key, value)
sb.set_session_storage_item(key, value)
sb.set_attributes(selector, attribute, value)
sb.is_attribute_present(selector, attribute, value=None)
sb.is_online()
sb.solve_captcha()
sb.click_captcha()
sb.gui_press_key(key)
sb.gui_press_keys(keys)
sb.gui_write(text)
sb.gui_click_x_y(x, y, timeframe=0.25)
sb.gui_click_element(selector, timeframe=0.25)
sb.gui_click_with_offset(selector, x, y, timeframe=0.25, center=False)
sb.gui_click_captcha()
sb.gui_drag_drop_points(x1, y1, x2, y2, timeframe=0.35)
sb.gui_drag_and_drop(drag_selector, drop_selector, timeframe=0.35)
sb.gui_click_and_hold(selector, timeframe=0.35)
sb.gui_hover_x_y(x, y)
sb.gui_hover_element(selector)
sb.gui_hover_and_click(hover_selector, click_selector)
sb.hover_element(selector)
sb.hover_and_click(hover_selector, click_selector)
sb.internalize_links()
sb.is_checked(selector)
sb.is_selected(selector)
sb.check_if_unchecked(selector)
sb.select_if_unselected(selector)
sb.uncheck_if_checked(selector)
sb.unselect_if_selected(selector)
sb.is_element_present(selector)
sb.is_element_visible(selector)
sb.is_text_visible(text, selector="body")
sb.is_exact_text_visible(text, selector="body")
sb.wait_for_text(text, selector="body", timeout=None)
sb.wait_for_text_not_visible(text, selector="body", timeout=None)
sb.wait_for_element_visible(selector, timeout=None)
sb.wait_for_element(selector, timeout=None)
sb.wait_for_element_not_visible(selector, timeout=None)
sb.wait_for_element_absent(selector, timeout=None)
sb.wait_for_any_of_elements_visible(*args, **kwargs)
sb.wait_for_any_of_elements_present(*args, **kwargs)
sb.assert_any_of_elements_visible(*args, **kwargs)
sb.assert_any_of_elements_present(*args, **kwargs)
sb.assert_element(selector, timeout=None)
sb.assert_element_visible(selector, timeout=None)
sb.assert_element_present(selector, timeout=None)
sb.assert_element_absent(selector, timeout=None)
sb.assert_element_not_visible(selector, timeout=None)
sb.assert_element_attribute(selector, attribute, value=None)
sb.assert_title(title)
sb.assert_title_contains(substring)
sb.assert_url(url)
sb.assert_url_contains(substring)
sb.assert_text(text, selector="html", timeout=None)
sb.assert_exact_text(text, selector="html", timeout=None)
sb.assert_text_not_visible(text, selector="body", timeout=None)
sb.assert_true(expression, msg=None)
sb.assert_false(expression, msg=None)
sb.assert_equal(first, second)
sb.assert_not_equal(first, second)
sb.assert_in(first, second)
sb.assert_not_in(first, second)
sb.js_scroll_into_view(selector)
sb.scroll_into_view(selector)
sb.scroll_to_y(y)
sb.scroll_to_top()
sb.scroll_to_bottom()
sb.scroll_up(amount=25)
sb.scroll_down(amount=25)
sb.save_page_source(name, folder=None)
sb.save_as_html(name, folder=None)
sb.save_screenshot(name, folder=None, selector=None)
sb.print_to_pdf(name, folder=None)
sb.save_as_pdf(name, folder=None)
sb.quit()  # (Pure CDP Mode only: `sb_cdp`)
```

ℹ️ When available, calling `sb.METHOD()` redirects to `sb.cdp.METHOD()` from UC + CDP Mode.

--------

<a id="Pure_CDP_Mode"></a>

### 🐙 <b translate="no">Pure CDP Mode</b> (<code translate="no">sb_cdp</code>)

In <b translate="no">Pure CDP Mode</b>, the browser is launched using CDP, and all browser actions are performed using CDP. WebDriver isn't available at all, but SeleniumBase can still call <code>PyAutoGUI</code> methods when CDP isn't enough.

🐙 Here's how to initialize Pure CDP Mode with a starting URL:

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(URL)
```

🐙 You can also initialize Pure CDP Mode and set the URL later:

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto(URL)
```

<b translate="no">Pure CDP Mode</b> includes all methods from regular CDP Mode. To quit a Pure CDP Mode browser before Python goes out-of-scope, use `sb.quit()`.

Basic example from [SeleniumBase/examples/cdp_mode/raw_cdp_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_turnstile.py):

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://seleniumbase.io/apps/turnstile")
sb.solve_captcha()
sb.assert_element("img#captcha-success")
sb.set_messenger_theme(location="top_left")
sb.post_message("SeleniumBase wasn't detected", duration=3)
sb.quit()
```

Another example: ([SeleniumBase/examples/cdp_mode/raw_cdp_methods.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_methods.py))

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://seleniumbase.io/demo_page")
sb.press_keys("input", "Text")
sb.highlight("button")
sb.type("textarea", "Here are some words")
sb.click("button")
sb.set_value("input#mySlider", "100")
sb.click_visible_elements("input.checkBoxClassB")
sb.select_option_by_text("#mySelect", "Set to 75%")
sb.gui_hover_and_click("#myDropdown", "#dropOption2")
sb.gui_click_element("#checkBox1")
sb.gui_drag_and_drop("img#logo", "div#drop2")
sb.nested_click("iframe#myFrame3", ".fBox")
sb.sleep(2)
sb.quit()
```

ℹ️ Even if you don't call `sb.quit()`, the browser still quits after the script goes out-of-scope.

--------

### 🐙 <b translate="no">CDP Mode</b> Async API / Methods

Initialization:

```python
from seleniumbase import cdp_driver

driver = await cdp_driver.start_async()
page = await driver.get(url, **kwargs)
```

Methods: (Sometimes `page` is named  `tab` in examples where `page` is already taken.)

```python
await page.get(url="about:blank")
await page.open(url="about:blank")  # Same as await page.get(url) in CDP Mode
await page.goto(url="about:blank")  # Same as await page.get(url) in CDP Mode
await page.find(text, best_match=False, timeout=10)  # text can be selector
await page.find_all(text, timeout=10)  # text can be selector
await page.select(selector, timeout=10)
await page.select_all(selector, timeout=10, include_frames=False)
await page.query_selector(selector)
await page.query_selector_all(selector)
await page.find_element_by_text(text, best_match=False)
await page.find_elements_by_text(text)
await page.send_keys(selector, text, timeout=5)
await page.type(selector, text, timeout=5)
await page.click(selector, timeout=5)
await page.click_if_visible(selector, timeout=0)
await page.click_with_offset(selector, x, y, center=False, timeout=5)
await page.solve_captcha()
await page.click_captcha()  # Same as solve_captcha()
await page.reload(ignore_cache=True, script_to_evaluate_on_load=None)
await page.evaluate(expression)
await page.js_dumps(obj_name)
await page.back()
await page.forward()
await page.get_window()
await page.get_content()
await page.maximize()
await page.minimize()
await page.fullscreen()
await page.medimize()
await page.set_window_size(left=0, top=0, width=1280, height=1024)
await page.set_window_rect(left=0, top=0, width=1280, height=1024)
await page.activate()
await page.bring_to_front()
await page.set_window_state(left=0, top=0, width=1280, height=720, state="normal")
await page.get_navigation_history()
await page.get_user_agent()
await page.get_cookie_string()
await page.get_locale_code()
await page.is_element_present(selector)
await page.is_element_visible(selector)
await page.is_online()
await page.open_external_inspector()  # Open separate browser for debugging
await page.close()
await page.scroll_down(amount=25)
await page.scroll_up(amount=25)
await page.wait_for(selector="", text="", timeout=10)
await page.set_attributes(selector, attribute, value)
await page.internalize_links()
await page.download_file(url, filename=None)
await page.save_screenshot(filename="auto", format="png", full_page=False)
await page.print_to_pdf(filename="auto")
await page.set_download_path(path)
await page.get_all_linked_sources()
await page.get_all_urls(absolute=True)
await page.get_html()
await page.get_page_source()
await page.get_element_rect(selector, timeout=5)  # (window-based)
await page.get_window_rect()
await page.get_gui_element_rect(selector, timeout=5)  # (screen-based)
await page.get_title()
await page.get_current_url()
await page.get_origin()
await page.get_document()
await page.get_flattened_document()
await page.get_local_storage()
await page.set_local_storage(items)
```

--------

### 🐙 <b translate="no">CDP Mode</b> WebElement API / Methods

After finding an element in CDP Mode, you can access `WebElement` methods:

(Eg. After `element = sb.find_element(selector)`)

```python
element.clear_input()
element.click()
element.click_with_offset(x, y, center=False)
element.flash(duration=0.5, color="EE4488")
element.focus()
element.gui_click(timeframe=0.25)
element.highlight_overlay()
element.is_in_viewport()
element.mouse_click()
element.mouse_drag(destination)
element.mouse_move()
element.press_keys(text)
element.query_selector(selector)
element.querySelector(selector)
element.query_selector_all(selector)
element.querySelectorAll(selector)
element.remove_from_dom()
element.save_screenshot(*args, **kwargs)
element.save_to_dom()
element.scroll_into_view()
element.select_option()
element.send_file(*file_paths)
element.send_keys(text)
element.set_text(value)
element.type(text)
element.get_position()
element.get_html()
element.get_js_attributes()
element.get_attribute(attribute)
element.get_parent()
```

--------

<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" alt="SeleniumBase" title="SeleniumBase" align="center" width="335">

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_gs.png" alt="SeleniumBase" title="SeleniumBase" width="335" /></a></div>
