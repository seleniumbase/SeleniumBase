<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> SeleniumBase CDP Mode Methods (CDP Mode API Reference)</h2>

Here's a list of SeleniumBase CDP Mode method definitions, which are defined in **[sb_cdp.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/sb_cdp.py)**

### 🐙 <b translate="no">CDP Mode</b> API / Methods

```python
sb.cdp.get(url, **kwargs)
sb.cdp.open(url, **kwargs)  # Same as sb.cdp.get(url, **kwargs)
sb.cdp.reload(ignore_cache=True, script_to_evaluate_on_load=None)
sb.cdp.refresh(*args, **kwargs)
sb.cdp.get_event_loop()
sb.cdp.get_rd_host()  # Returns the remote-debugging host
sb.cdp.get_rd_port()  # Returns the remote-debugging port
sb.cdp.get_rd_url()  # Returns the remote-debugging URL
sb.cdp.get_endpoint_url()  # Same as sb.cdp.get_rd_url()
sb.cdp.get_port()  # Same as sb.cdp.get_rd_port()
sb.cdp.add_handler(event, handler)
sb.cdp.find_element(selector, best_match=False, timeout=None)
sb.cdp.find(selector, best_match=False, timeout=None)
sb.cdp.locator(selector, best_match=False, timeout=None)
sb.cdp.find_element_by_text(text, tag_name=None, timeout=None)
sb.cdp.find_all(selector, timeout=None)
sb.cdp.find_elements_by_text(text, tag_name=None)
sb.cdp.select(selector, timeout=None)
sb.cdp.select_all(selector, timeout=None)
sb.cdp.find_elements(selector, timeout=None)
sb.cdp.find_visible_elements(selector, timeout=None)
sb.cdp.click(selector, timeout=None)
sb.cdp.click_if_visible(selector)
sb.cdp.click_visible_elements(selector, limit=0)
sb.cdp.click_nth_element(selector, number)
sb.cdp.click_nth_visible_element(selector, number)
sb.cdp.click_with_offset(selector, x, y, center=False)
sb.cdp.click_link(link_text)
sb.cdp.go_back()
sb.cdp.go_forward()
sb.cdp.get_navigation_history()
sb.cdp.tile_windows(windows=None, max_columns=0)
sb.cdp.grant_permissions(permissions, origin=None)
sb.cdp.grant_all_permissions()
sb.cdp.reset_permissions()
sb.cdp.get_all_cookies(*args, **kwargs)
sb.cdp.set_all_cookies(*args, **kwargs)
sb.cdp.save_cookies(*args, **kwargs)
sb.cdp.load_cookies(*args, **kwargs)
sb.cdp.clear_cookies()
sb.cdp.sleep(seconds)
sb.cdp.bring_active_window_to_front()
sb.cdp.bring_to_front()
sb.cdp.get_active_element()
sb.cdp.get_active_element_css()
sb.cdp.click_active_element()
sb.cdp.mouse_click(selector, timeout=None)
sb.cdp.nested_click(parent_selector, selector)
sb.cdp.get_nested_element(parent_selector, selector)
sb.cdp.select_option_by_text(dropdown_selector, option)
sb.cdp.select_option_by_index(dropdown_selector, option)
sb.cdp.select_option_by_value(dropdown_selector, option)
sb.cdp.flash(selector, duration=1, color="44CC88", pause=0)
sb.cdp.highlight(selector)
sb.cdp.focus(selector)
sb.cdp.highlight_overlay(selector)
sb.cdp.get_parent(element)
sb.cdp.remove_element(selector)
sb.cdp.remove_from_dom(selector)
sb.cdp.remove_elements(selector)
sb.cdp.send_keys(selector, text, timeout=None)
sb.cdp.press_keys(selector, text, timeout=None)
sb.cdp.type(selector, text, timeout=None)
sb.cdp.set_value(selector, text, timeout=None)
sb.cdp.clear_input(selector, timeout=None)
sb.cdp.clear(selector, timeout=None)
sb.cdp.submit(selector)
sb.cdp.evaluate(expression)
sb.cdp.execute_script(expression)
sb.cdp.js_dumps(obj_name)
sb.cdp.maximize()
sb.cdp.minimize()
sb.cdp.medimize()
sb.cdp.set_window_rect(x, y, width, height)
sb.cdp.reset_window_size()
sb.cdp.open_new_window(url=None, switch_to=True)
sb.cdp.switch_to_window(window)
sb.cdp.switch_to_newest_window()
sb.cdp.open_new_tab(url=None, switch_to=True)
sb.cdp.switch_to_tab(tab)
sb.cdp.switch_to_newest_tab()
sb.cdp.close_active_tab()
sb.cdp.get_active_tab()
sb.cdp.get_tabs()
sb.cdp.get_window()
sb.cdp.get_text(selector)
sb.cdp.get_title()
sb.cdp.get_current_url()
sb.cdp.get_origin()
sb.cdp.get_html(include_shadow_dom=True)
sb.cdp.get_page_source(include_shadow_dom=True)
sb.cdp.get_user_agent()
sb.cdp.get_cookie_string()
sb.cdp.get_locale_code()
sb.cdp.get_local_storage_item(key)
sb.cdp.get_session_storage_item(key)
sb.cdp.get_screen_rect()
sb.cdp.get_window_rect()
sb.cdp.get_window_size()
sb.cdp.get_window_position()
sb.cdp.get_element_rect(selector, timeout=None)
sb.cdp.get_element_size(selector, timeout=None)
sb.cdp.get_element_position(selector, timeout=None)
sb.cdp.get_gui_element_rect(selector, timeout=None)
sb.cdp.get_gui_element_center(selector, timeout=None)
sb.cdp.get_document()
sb.cdp.get_flattened_document()
sb.cdp.get_element_attributes(selector)
sb.cdp.get_element_attribute(selector, attribute)
sb.cdp.get_attribute(selector, attribute)
sb.cdp.get_element_html(selector)
sb.cdp.get_mfa_code(totp_key=None)
sb.cdp.enter_mfa_code(selector, totp_key=None, timeout=None)
sb.cdp.activate_messenger()
sb.cdp.set_messenger_theme(theme="default", location="default")
sb.cdp.post_message(message, duration=None, pause=True, style="info")
sb.cdp.set_locale(locale)
sb.cdp.set_local_storage_item(key, value)
sb.cdp.set_session_storage_item(key, value)
sb.cdp.set_attributes(selector, attribute, value)
sb.cdp.is_attribute_present(selector, attribute, value=None)
sb.cdp.is_online()
sb.cdp.solve_captcha()
sb.cdp.click_captcha()
sb.cdp.gui_press_key(key)
sb.cdp.gui_press_keys(keys)
sb.cdp.gui_write(text)
sb.cdp.gui_click_x_y(x, y, timeframe=0.25)
sb.cdp.gui_click_element(selector, timeframe=0.25)
sb.cdp.gui_click_with_offset(selector, x, y, timeframe=0.25, center=False)
sb.cdp.gui_click_captcha()
sb.cdp.gui_drag_drop_points(x1, y1, x2, y2, timeframe=0.35)
sb.cdp.gui_drag_and_drop(drag_selector, drop_selector, timeframe=0.35)
sb.cdp.gui_click_and_hold(selector, timeframe=0.35)
sb.cdp.gui_hover_x_y(x, y)
sb.cdp.gui_hover_element(selector)
sb.cdp.gui_hover_and_click(hover_selector, click_selector)
sb.cdp.internalize_links()
sb.cdp.is_checked(selector)
sb.cdp.is_selected(selector)
sb.cdp.check_if_unchecked(selector)
sb.cdp.select_if_unselected(selector)
sb.cdp.uncheck_if_checked(selector)
sb.cdp.unselect_if_selected(selector)
sb.cdp.is_element_present(selector)
sb.cdp.is_element_visible(selector)
sb.cdp.is_text_visible(text, selector="body")
sb.cdp.is_exact_text_visible(text, selector="body")
sb.cdp.wait_for_text(text, selector="body", timeout=None)
sb.cdp.wait_for_text_not_visible(text, selector="body", timeout=None)
sb.cdp.wait_for_element_visible(selector, timeout=None)
sb.cdp.wait_for_element(selector, timeout=None)
sb.cdp.wait_for_element_not_visible(selector, timeout=None)
sb.cdp.wait_for_element_absent(selector, timeout=None)
sb.cdp.wait_for_any_of_elements_visible(*args, **kwargs)
sb.cdp.wait_for_any_of_elements_present(*args, **kwargs)
sb.cdp.assert_any_of_elements_visible(*args, **kwargs)
sb.cdp.assert_any_of_elements_present(*args, **kwargs)
sb.cdp.assert_element(selector, timeout=None)
sb.cdp.assert_element_visible(selector, timeout=None)
sb.cdp.assert_element_present(selector, timeout=None)
sb.cdp.assert_element_absent(selector, timeout=None)
sb.cdp.assert_element_not_visible(selector, timeout=None)
sb.cdp.assert_element_attribute(selector, attribute, value=None)
sb.cdp.assert_title(title)
sb.cdp.assert_title_contains(substring)
sb.cdp.assert_url(url)
sb.cdp.assert_url_contains(substring)
sb.cdp.assert_text(text, selector="html", timeout=None)
sb.cdp.assert_exact_text(text, selector="html", timeout=None)
sb.cdp.assert_text_not_visible(text, selector="body", timeout=None)
sb.cdp.assert_true()
sb.cdp.assert_false()
sb.cdp.assert_equal(first, second)
sb.cdp.assert_not_equal(first, second)
sb.cdp.assert_in(first, second)
sb.cdp.assert_not_in(first, second)
sb.cdp.scroll_into_view(selector)
sb.cdp.scroll_to_y(y)
sb.cdp.scroll_by_y(y)
sb.cdp.scroll_to_top()
sb.cdp.scroll_to_bottom()
sb.cdp.scroll_up(amount=25)
sb.cdp.scroll_down(amount=25)
sb.cdp.save_page_source(name, folder=None)
sb.cdp.save_as_html(name, folder=None)
sb.cdp.save_screenshot(name, folder=None, selector=None)
sb.cdp.print_to_pdf(name, folder=None)
sb.cdp.save_as_pdf(name, folder=None)
```

ℹ️ When available, calling `sb.METHOD()` redirects to `sb.cdp.METHOD()` because regular SB methods automatically call their CDP Mode counterparts to maintain stealth when CDP Mode is active.

--------

<a id="Pure_CDP_Mode"></a>

### 🐙 <b translate="no">Pure CDP Mode</b> (<code translate="no">sb_cdp</code>)

<b translate="no">Pure CDP Mode</b> doesn't use WebDriver for anything. The browser is launched using CDP, and all browser actions are performed using CDP (or <code>PyAutoGUI</code>). Initialization:

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(url=None, **kwargs)
```

<b translate="no">Pure CDP Mode</b> includes all methods from regular CDP Mode, except that they're called directly from <code>sb</code> instead of <code>sb.cdp</code>. Eg: <code>sb.gui_click_captcha()</code>. To quit a CDP-launched browser, use `sb.driver.stop()`.

Basic example from [SeleniumBase/examples/cdp_mode/raw_cdp_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_turnstile.py):

```python
from seleniumbase import sb_cdp

url = "https://seleniumbase.io/apps/turnstile"
sb = sb_cdp.Chrome(url)
sb.solve_captcha()
sb.assert_element("img#captcha-success")
sb.set_messenger_theme(location="top_left")
sb.post_message("SeleniumBase wasn't detected", duration=3)
sb.driver.stop()
```

Another example: ([SeleniumBase/examples/cdp_mode/raw_cdp_methods.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_methods.py))

```python
from seleniumbase import sb_cdp

url = "https://seleniumbase.io/demo_page"
sb = sb_cdp.Chrome(url)
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
sb.driver.stop()
```

ℹ️ Even if you don't call `sb.driver.stop()`, the browser still quits after the script goes out-of-scope.

--------

### 🐙 <b translate="no">CDP Mode</b> Async API / Methods

Initialization:

```python
from seleniumbase import cdp_driver

driver = await cdp_driver.start_async()
tab = await driver.get(url, **kwargs)
```

Methods: (Sometimes `tab` is named `page` in examples)

```python
await tab.get(url="about:blank")
await tab.open(url="about:blank")
await tab.find(text, best_match=False, timeout=10)  # text can be selector
await tab.find_all(text, timeout=10)  # text can be selector
await tab.select(selector, timeout=10)
await tab.select_all(selector, timeout=10, include_frames=False)
await tab.query_selector(selector)
await tab.query_selector_all(selector)
await tab.find_element_by_text(text, best_match=False)
await tab.find_elements_by_text(text)
await tab.reload(ignore_cache=True, script_to_evaluate_on_load=None)
await tab.evaluate(expression)
await tab.js_dumps(obj_name)
await tab.back()
await tab.forward()
await tab.get_window()
await tab.get_content()
await tab.maximize()
await tab.minimize()
await tab.fullscreen()
await tab.medimize()
await tab.set_window_size(left=0, top=0, width=1280, height=1024)
await tab.set_window_rect(left=0, top=0, width=1280, height=1024)
await tab.activate()
await tab.bring_to_front()
await tab.set_window_state(
    left=0, top=0, width=1280, height=720, state="normal")
await tab.get_navigation_history()
await tab.open_external_inspector()  # Open separate browser for debugging
await tab.close()
await tab.scroll_down(amount=25)
await tab.scroll_up(amount=25)
await tab.wait_for(selector="", text="", timeout=10)
await tab.download_file(url, filename=None)
await tab.save_screenshot(
    filename="auto", format="png", full_page=False)
await tab.print_to_pdf(filename="auto")
await tab.set_download_path(path)
await tab.get_all_linked_sources()
await tab.get_all_urls(absolute=True)
await tab.get_html()
await tab.get_page_source()
await tab.is_element_present(selector)
await tab.is_element_visible(selector)
await tab.get_element_rect(selector, timeout=5)  # (window-based)
await tab.get_window_rect()
await tab.get_gui_element_rect(selector, timeout=5)  # (screen-based)
await tab.get_title()
await tab.get_current_url()
await tab.send_keys(selector, text, timeout=5)
await tab.type(selector, text, timeout=5)
await tab.click(selector, timeout=5)
await tab.click_with_offset(selector, x, y, center=False, timeout=5)
await tab.solve_captcha()
await tab.click_captcha()  # Same as solve_captcha()
await tab.get_document()
await tab.get_flattened_document()
await tab.get_local_storage()
await tab.set_local_storage(items)
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
