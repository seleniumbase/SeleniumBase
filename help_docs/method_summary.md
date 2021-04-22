[<img src="https://seleniumbase.io/cdn/img/sb_text_f.png" title="SeleniumBase" align="center" width="360">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Method Summary (API Reference)</h2>

[<img src="https://seleniumbase.io/cdn/img/sb_api_youtube.png" title="SeleniumBase Features" width="285">](https://www.youtube.com/watch?v=_yNJlHnp2JA)
<p>(<b><a href="https://www.youtube.com/watch?v=_yNJlHnp2JA">Common API Methods on YouTube</a></b>)</p>

Here's a list of SeleniumBase method definitions, which are defined in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py)

For backwards compatibility, older versions of method names have remained to keep older scripts working. *(E.g: wait_for_element_visible was shortened to wait_for_element and then to find_element.)*

```python
self.open(url)
# Duplicates: self.open_url(url), self.visit(url), visit_url(url),
#             self.goto(url), self.go_to(url)

self.get(url)
# If the url parameter is a URL: Perform self.open(url)
# Otherwise: return self.get_element(URL_AS_A_SELECTOR)

self.click(selector, by=By.CSS_SELECTOR, timeout=None, delay=0)

self.slow_click(selector, by=By.CSS_SELECTOR, timeout=None)

self.double_click(selector, by=By.CSS_SELECTOR, timeout=None)

self.click_chain(selectors_list, by=By.CSS_SELECTOR, timeout=None, spacing=0)

self.type(selector, text, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.update_text(selector, text, by=By.CSS_SELECTOR, timeout=None)
#             self.input(selector, text, by=By.CSS_SELECTOR, timeout=None)
#             self.fill(selector, text, by=By.CSS_SELECTOR, timeout=None)
#             self.write(selector, text, by=By.CSS_SELECTOR, timeout=None)

self.add_text(selector, text, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.send_keys(selector, text, by=By.CSS_SELECTOR, timeout=None)

self.submit(selector, by=By.CSS_SELECTOR)

self.clear(selector, by=By.CSS_SELECTOR, timeout=None)

self.focus(selector, by=By.CSS_SELECTOR, timeout=None)

self.refresh_page()
# Duplicates: self.refresh(), self.reload(), self.reload_page()

self.get_current_url()

self.get_page_source()

self.get_title()
# Duplicates: self.get_page_title()

self.get_user_agent()

self.get_locale_code()

self.go_back()

self.go_forward()

self.open_start_page()

self.is_element_present(selector, by=By.CSS_SELECTOR)

self.is_element_visible(selector, by=By.CSS_SELECTOR)

self.is_element_enabled(selector, by=By.CSS_SELECTOR)

self.is_text_visible(text, selector="html", by=By.CSS_SELECTOR)

self.is_link_text_visible(link_text)

self.is_partial_link_text_visible(partial_link_text)

self.is_link_text_present(link_text)

self.is_partial_link_text_present(link_text)

self.get_link_attribute(link_text, attribute, hard_fail=True)
# Duplicates: self.get_link_text_attribute(link_text, attribute, hard_fail=True)

self.get_partial_link_text_attribute(link_text, attribute, hard_fail=True)

self.click_link(link_text, timeout=None)
# Duplicates: self.click_link_text(link_text, timeout=None)

self.click_partial_link(partial_link_text, timeout=None)
# Duplicates: self.click_partial_link_text(partial_link_text, timeout=None)

self.get_text(selector, by=By.CSS_SELECTOR, timeout=None)

self.get_attribute(selector, attribute, by=By.CSS_SELECTOR, timeout=None, hard_fail=True)

self.set_attribute(selector, attribute, value, by=By.CSS_SELECTOR, timeout=None)

self.set_attributes(selector, attribute, value, by=By.CSS_SELECTOR)
# Duplicates: self.set_attribute_all(selector, attribute, value, by=By.CSS_SELECTOR)

self.remove_attribute(selector, attribute, by=By.CSS_SELECTOR, timeout=None)

self.remove_attributes(selector, attribute, by=By.CSS_SELECTOR)

self.get_property_value(selector, property, by=By.CSS_SELECTOR, timeout=None)

self.get_image_url(selector, by=By.CSS_SELECTOR, timeout=None)

self.find_elements(selector, by=By.CSS_SELECTOR, limit=0)

self.find_visible_elements(selector, by=By.CSS_SELECTOR, limit=0)

self.click_visible_elements(selector, by=By.CSS_SELECTOR, limit=0, timeout=None)

self.click_nth_visible_element(selector, number, by=By.CSS_SELECTOR, timeout=None)

self.click_if_visible(selector, by=By.CSS_SELECTOR)

self.is_selected(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.is_checked(selector, by=By.CSS_SELECTOR, timeout=None)

self.select_if_unselected(selector, by=By.CSS_SELECTOR)
# Duplicates: self.check_if_unchecked(selector, by=By.CSS_SELECTOR)

self.unselect_if_selected(selector, by=By.CSS_SELECTOR)
# Duplicates: self.uncheck_if_checked(selector, by=By.CSS_SELECTOR)

self.is_element_in_an_iframe(selector, by=By.CSS_SELECTOR)

self.switch_to_frame_of_element(selector, by=By.CSS_SELECTOR)

self.hover_on_element(selector, by=By.CSS_SELECTOR)

self.hover_and_click(hover_selector, click_selector,
                     hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                     timeout=None)

self.hover_and_double_click(hover_selector, click_selector,
                            hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                            timeout=None)

self.drag_and_drop(drag_selector, drop_selector,
                   drag_by=By.CSS_SELECTOR, drop_by=By.CSS_SELECTOR,
                   timeout=None)

self.drag_and_drop_with_offset(selector, x, y, by=By.CSS_SELECTOR, timeout=None)

self.select_option_by_text(dropdown_selector, option,
                           dropdown_by=By.CSS_SELECTOR,
                           timeout=None)

self.select_option_by_index(dropdown_selector, option,
                            dropdown_by=By.CSS_SELECTOR,
                            timeout=None)

self.select_option_by_value(dropdown_selector, option,
                            dropdown_by=By.CSS_SELECTOR,
                            timeout=None)

self.load_html_string(html_string, new_page=True)

self.set_content(html_string, new_page=False)

self.load_html_file(html_file, new_page=True)

self.open_html_file(html_file)

self.execute_script(script, *args, **kwargs)

self.execute_async_script(script, timeout=None)

self.safe_execute_script(script, *args, **kwargs)

self.set_window_rect(x, y, width, height)

self.set_window_size(width, height)

self.maximize_window()

self.switch_to_frame(frame, timeout=None)

self.switch_to_default_content()

self.open_new_window(switch_to=True)

self.switch_to_window(window, timeout=None)

self.switch_to_default_window()

self.switch_to_newest_window()

self.get_new_driver(browser=None, headless=None, locale_code=None,
                    servername=None, port=None, proxy=None, agent=None,
                    switch_to=True, cap_file=None, cap_string=None,
                    disable_csp=None, enable_ws=None, enable_sync=None,
                    use_auto_ext=None, no_sandbox=None, disable_gpu=None,
                    incognito=None, guest_mode=None,
                    devtools=None, remote_debug=None,
                    swiftshader=None, block_images=None, user_data_dir=None,
                    extension_zip=None, extension_dir=None, is_mobile=False,
                    d_width=None, d_height=None, d_p_r=None)

self.switch_to_driver(driver)

self.switch_to_default_driver()

self.save_screenshot(name, folder=None)

self.save_page_source(name, folder=None)

self.save_cookies(name="cookies.txt")

self.load_cookies(name="cookies.txt")

self.delete_all_cookies()

self.delete_saved_cookies(name="cookies.txt")

self.wait_for_ready_state_complete(timeout=None)

self.wait_for_angularjs(timeout=None)

self.sleep(seconds)
# Duplicates: self.wait(seconds)

self.install_addon(xpi_file)

self.activate_design_mode()

self.deactivate_design_mode()

self.activate_jquery()

self.bring_to_front(selector, by=By.CSS_SELECTOR)

self.highlight_click(selector, by=By.CSS_SELECTOR, loops=3, scroll=True)

self.highlight_update_text(selector, text, by=By.CSS_SELECTOR, loops=3, scroll=True)

self.highlight(selector, by=By.CSS_SELECTOR, loops=4, scroll=True)

self.press_up_arrow(selector="html", times=1, by=By.CSS_SELECTOR)

self.press_down_arrow(selector="html", times=1, by=By.CSS_SELECTOR)

self.press_left_arrow(selector="html", times=1, by=By.CSS_SELECTOR)

self.press_right_arrow(selector="html", times=1, by=By.CSS_SELECTOR)

self.scroll_to(selector, by=By.CSS_SELECTOR)

self.slow_scroll_to(selector, by=By.CSS_SELECTOR)

self.scroll_to_top()

self.scroll_to_bottom()

self.click_xpath(xpath)

self.js_click(selector, by=By.CSS_SELECTOR, all_matches=False)

self.js_click_all(selector, by=By.CSS_SELECTOR)

self.jquery_click(selector, by=By.CSS_SELECTOR)

self.jquery_click_all(selector, by=By.CSS_SELECTOR)

self.hide_element(selector, by=By.CSS_SELECTOR)

self.hide_elements(selector, by=By.CSS_SELECTOR)

self.show_element(selector, by=By.CSS_SELECTOR)

self.show_elements(selector, by=By.CSS_SELECTOR)

self.remove_element(selector, by=By.CSS_SELECTOR)

self.remove_elements(selector, by=By.CSS_SELECTOR)

self.ad_block()
# Duplicates: self.block_ads()

self.get_domain_url(url)

self.get_beautiful_soup(source=None)

self.get_unique_links()

self.get_link_status_code(link, allow_redirects=False, timeout=5)

self.assert_link_status_code_is_not_404(link)

self.assert_no_404_errors(multithreaded=True)
# Duplicates: self.assert_no_broken_links(multithreaded=True)

self.print_unique_links_with_status_codes()

self.get_pdf_text(pdf, page=None, maxpages=None, password=None,
                  codec='utf-8', wrap=False, nav=False, override=False)

self.assert_pdf_text(pdf, text, page=None, maxpages=None, password=None,
                     codec='utf-8', wrap=True, nav=False, override=False)

self.create_folder(folder)

self.choose_file(selector, file_path, by=By.CSS_SELECTOR, timeout=None)

self.save_element_as_image_file(selector, file_name, folder=None, overlay_text="")

self.download_file(file_url, destination_folder=None)

self.save_file_as(file_url, new_file_name, destination_folder=None)

self.save_data_as(data, file_name, destination_folder=None)

self.get_downloads_folder()

self.get_browser_downloads_folder()

self.get_path_of_downloaded_file(file, browser=False)

self.is_downloaded_file_present(file, browser=False)

self.delete_downloaded_file_if_present(file, browser=False)

self.assert_downloaded_file(file, timeout=None, browser=False)

self.assert_true(expr, msg=None)

self.assert_false(expr, msg=None)

self.assert_equal(first, second, msg=None)

self.assert_not_equal(first, second, msg=None)

self.assert_raises(*args, **kwargs)

self.assert_title(title)

self.assert_no_js_errors()

self.inspect_html()

self.is_chromium()

self.get_google_auth_password(totp_key=None)

self.convert_css_to_xpath(css)

self.convert_xpath_to_css(xpath)

self.convert_to_css_selector(selector, by)

self.set_value(selector, text, by=By.CSS_SELECTOR, timeout=None)

self.js_update_text(selector, text, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.js_type(selector, text, by=By.CSS_SELECTOR, timeout=None)
#             self.set_text(selector, text, by=By.CSS_SELECTOR, timeout=None)

self.jquery_update_text(selector, text, by=By.CSS_SELECTOR, timeout=None)

self.set_time_limit(time_limit)

self.set_default_timeout(timeout)

self.reset_default_timeout()

self.skip(reason="")

############

self.set_local_storage_item(key, value)

self.get_local_storage_item(key)

self.remove_local_storage_item(key)

self.clear_local_storage()

self.get_local_storage_keys()

self.get_local_storage_items()

self.set_session_storage_item(key, value)

self.get_session_storage_item(key)

self.remove_session_storage_item(key)

self.clear_session_storage()

self.get_session_storage_keys()

self.get_session_storage_items()

############

self.add_css_link(css_link)

self.add_js_link(js_link)

self.add_css_style(css_style)

self.add_js_code_from_link(js_link)

self.add_js_code(js_code)

self.add_meta_tag(http_equiv=None, content=None)

############

self.create_presentation(name=None, theme="default", transition="default")

self.add_slide(content=None, image=None, code=None, iframe=None,
               content2=None, notes=None, transition=None, name=None)

self.save_presentation(name=None, filename=None, show_notes=False, interval=0)

self.begin_presentation(name=None, filename=None, show_notes=False, interval=0)

############

self.create_pie_chart(chart_name=None, title=None, subtitle=None,
                      data_name=None, unit=None, libs=True,
                      labels=True, legend=True)

self.create_bar_chart(chart_name=None, title=None, subtitle=None,
                      data_name=None, unit=None, libs=True,
                      labels=True, legend=True)

self.create_column_chart(chart_name=None, title=None, subtitle=None,
                         data_name=None, unit=None, libs=True,
                         labels=True, legend=True)

self.create_line_chart(chart_name=None, title=None, subtitle=None,
                       data_name=None, unit=None, zero=False, libs=True,
                       labels=True, legend=True)

self.create_area_chart(chart_name=None, title=None, subtitle=None,
                       data_name=None, unit=None, zero=False, libs=True,
                       labels=True, legend=True)

self.add_series_to_chart(data_name=None, chart_name=None)

self.add_data_point(label, value, color=None, chart_name=None)

self.save_chart(chart_name=None, filename=None, folder=None)

self.display_chart(chart_name=None, filename=None, interval=0)

self.extract_chart(chart_name=None)

############

self.create_tour(name=None, theme=None)

self.create_shepherd_tour(name=None, theme=None)

self.create_bootstrap_tour(name=None)

self.create_hopscotch_tour(name=None)

self.create_introjs_tour(name=None)

self.add_tour_step(message, selector=None, name=None,
                   title=None, theme=None, alignment=None)

self.play_tour(name=None)

self.export_tour(name=None, filename="my_tour.js", url=None)

self.activate_jquery_confirm()

self.activate_messenger()

self.post_message(message, duration=None, pause=True, style="info")

self.post_message_and_highlight(message, selector, by=By.CSS_SELECTOR)

self.post_success_message(message, duration=None, pause=True)

self.post_error_message(message, duration=None, pause=True)

self.set_messenger_theme(theme="default", location="default",
                         max_messages="default")

############

self.generate_referral(start_page, destination_page, selector=None)

self.generate_traffic(start_page, destination_page, loops=1, selector=None)

self.generate_referral_chain(pages)

self.generate_traffic_chain(pages, loops=1)

############

self.get_element(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.wait_for_element_present(selector, by=By.CSS_SELECTOR, timeout=None)

self.assert_element_present(selector, by=By.CSS_SELECTOR, timeout=None)

self.assert_elements_present(*args, **kwargs)

############

self.find_element(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.wait_for_element(selector, by=By.CSS_SELECTOR, timeout=None)
#             self.wait_for_element_visible(selector, by=By.CSS_SELECTOR, timeout=None)

self.assert_element(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.assert_element_visible(selector, by=By.CSS_SELECTOR, timeout=None)

self.assert_elements(*args, **kwargs)
# Duplicates: self.assert_elements_visible(*args, **kwargs)

############

self.find_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.wait_for_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)
#             self.wait_for_text_visible(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

self.wait_for_exact_text_visible(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

self.assert_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.assert_text_visible(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

self.assert_exact_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

############

self.wait_for_link_text_present(link_text, timeout=None)

self.wait_for_partial_link_text_present(link_text, timeout=None)

self.find_link_text(link_text, timeout=None)
# Duplicates: self.wait_for_link_text(link_text, timeout=None)
#             self.wait_for_link_text_visible(link_text, timeout=None)

self.assert_link_text(link_text, timeout=None)

############

self.find_partial_link_text(partial_link_text, timeout=None)
# Duplicates: self.wait_for_partial_link_text(partial_link_text, timeout=None)

self.assert_partial_link_text(partial_link_text, timeout=None)

############

self.wait_for_element_absent(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.wait_for_element_not_present(selector, by=By.CSS_SELECTOR)

self.assert_element_absent(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.assert_element_not_present(selector, by=By.CSS_SELECTOR)

############

self.wait_for_element_not_visible(selector, by=By.CSS_SELECTOR, timeout=None)

self.assert_element_not_visible(selector, by=By.CSS_SELECTOR, timeout=None)

############

self.wait_for_text_not_visible(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

self.assert_text_not_visible(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

############

self.accept_alert(timeout=None)
# Duplicates: self.wait_for_and_accept_alert(timeout=None)

self.dismiss_alert(timeout=None)
# Duplicates: self.wait_for_and_dismiss_alert(timeout=None)

self.switch_to_alert(timeout=None)
# Duplicates: self.wait_for_and_switch_to_alert(timeout=None)

############

self.check_window(name="default", level=0, baseline=False)

############

self.deferred_assert_element(selector, by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.delayed_assert_element(selector, by=By.CSS_SELECTOR, timeout=None)

self.deferred_assert_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)
# Duplicates: self.delayed_assert_text(text, selector="html", by=By.CSS_SELECTOR, timeout=None)

self.process_deferred_asserts(print_only=False)
# Duplicates: self.process_delayed_asserts(print_only=False)

############

self.fail(msg=None)  # Inherited from "unittest"

self._print(TEXT)  # Calls Python's print() / Allows for translations
```

--------

<h2>🔵 Examples</h2>

✅ Test Folder: [SeleniumBase/examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)

* [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py)
* [parameterized_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/parameterized_test.py)
* [test_deferred_asserts.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_deferred_asserts.py)
* [test_demo_site.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py)
* [test_error_page.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_error_page.py)
* [test_login.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_login.py)
* [test_markers.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_markers.py)
* [test_swag_labs.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py)
* [test_suite.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_suite.py)
* [test_tinymce.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_tinymce.py)
* And many more...
