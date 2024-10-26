<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) SeleniumBase Methods (API Reference)

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=_yNJlHnp2JA"><img src="https://seleniumbase.github.io/cdn/img/sb_api_youtube.png" title="SeleniumBase on YouTube" width="285" /></a>
<!-- GitHub Only --><p>(<b><a href="https://www.youtube.com/watch?v=_yNJlHnp2JA">Common API Methods on YouTube</a></b>)</p>

Here's a list of SeleniumBase method definitions, which are defined in **[base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py)**

For backwards compatibility, older versions of method names have remained to keep older scripts working. *(E.g: wait_for_element_visible was shortened to wait_for_element and then to find_element.)*

```python
self.open(url)
# Duplicates: self.open_url(url), self.visit(url), visit_url(url),
#             self.goto(url), self.go_to(url)

self.get(url)
# If the url parameter is a URL: Perform self.open(url)
# Otherwise: return self.get_element(URL_AS_A_SELECTOR)

self.click(selector, by="css selector", timeout=None, delay=0, scroll=True)

self.slow_click(selector, by="css selector", timeout=None)

self.double_click(selector, by="css selector", timeout=None)

self.context_click(selector, by="css selector", timeout=None)
# Duplicates:
# self.right_click(selector, by="css selector", timeout=None)

self.click_chain(selectors_list, by="css selector", timeout=None, spacing=0)

self.type(selector, text, by="css selector", timeout=None)
# Duplicates:
# self.update_text(selector, text, by="css selector", timeout=None)
# self.input(selector, text, by="css selector", timeout=None)
# self.fill(selector, text, by="css selector", timeout=None)
# self.write(selector, text, by="css selector", timeout=None)

self.send_keys(selector, text, by="css selector", timeout=None)
# Duplicates:
# self.add_text(selector, text, by="css selector", timeout=None)

self.press_keys(selector, text, by="css selector", timeout=None)

self.submit(selector, by="css selector")

self.clear(selector, by="css selector", timeout=None)

self.focus(selector, by="css selector", timeout=None)

self.refresh()
# Duplicates: self.refresh_page(), self.reload_page(), self.reload()

self.get_current_url()

self.get_origin()

self.get_page_source()

self.get_title()
# Duplicates: self.get_page_title()

self.get_user_agent()

self.get_locale_code()

self.go_back()

self.go_forward()

self.open_start_page()

self.open_if_not_url(url)

self.is_element_present(selector, by="css selector")

self.is_element_visible(selector, by="css selector")

self.is_element_clickable(selector, by="css selector")

self.is_element_enabled(selector, by="css selector")

self.is_text_visible(text, selector="html", by="css selector")

self.is_exact_text_visible(text, selector="html", by="css selector")

self.is_non_empty_text_visible(selector="html", by="css selector")

self.is_attribute_present(selector, attribute, value=None, by="css selector")

self.is_link_text_visible(link_text)

self.is_partial_link_text_visible(partial_link_text)

self.is_link_text_present(link_text)

self.is_partial_link_text_present(link_text)

self.get_link_attribute(link_text, attribute, hard_fail=True)
# Duplicates:
# self.get_link_text_attribute(link_text, attribute, hard_fail=True)

self.get_partial_link_text_attribute(link_text, attribute, hard_fail=True)

self.click_link(link_text, timeout=None)
# Duplicates:
# self.click_link_text(link_text, timeout=None)

self.click_partial_link(partial_link_text, timeout=None)
# Duplicates:
# self.click_partial_link_text(partial_link_text, timeout=None)

self.get_text(selector="html", by="css selector", timeout=None)

self.get_attribute(selector, attribute, by="css selector", timeout=None, hard_fail=True)

self.set_attribute(selector, attribute, value, by="css selector", timeout=None, scroll=False)

self.set_attributes(selector, attribute, value, by="css selector")
# Duplicates:
# self.set_attribute_all(selector, attribute, value, by="css selector")

self.remove_attribute(selector, attribute, by="css selector", timeout=None)

self.remove_attributes(selector, attribute, by="css selector")

self.internalize_links()

self.get_property(selector, property, by="css selector", timeout=None)

self.get_text_content(selector="html", by="css selector", timeout=None)

self.get_property_value(selector, property, by="css selector", timeout=None)

self.get_image_url(selector, by="css selector", timeout=None)

self.find_elements(selector, by="css selector", limit=0)
# Duplicates:
# self.select_all(selector, by="css selector", limit=0)

self.find_visible_elements(selector, by="css selector", limit=0)

self.click_visible_elements(selector, by="css selector", limit=0, timeout=None)

self.click_nth_visible_element(selector, number, by="css selector", timeout=None)

self.click_if_visible(selector, by="css selector", timeout=0)

self.click_active_element()

self.click_with_offset(
    selector, x, y, by="css selector", mark=None, timeout=None, center=None)

self.double_click_with_offset(
    selector, x, y, by="css selector", mark=None, timeout=None, center=None)

self.is_checked(selector, by="css selector", timeout=None)
# Duplicates:
# self.is_selected(selector, by="css selector", timeout=None)

self.check_if_unchecked(selector, by="css selector")
# Duplicates:
# self.select_if_unselected(selector, by="css selector")

self.uncheck_if_checked(selector, by="css selector")
# Duplicates:
# self.unselect_if_selected(selector, by="css selector")

self.is_element_in_an_iframe(selector, by="css selector")

self.switch_to_frame_of_element(selector, by="css selector")

self.hover(selector, by="css selector", timeout=None)
# Duplicates:
# self.hover_on_element(selector, by="css selector", timeout=None)
# self.hover_over_element(selector, by="css selector", timeout=None)

self.hover_and_click(
    hover_selector, click_selector,
    hover_by="css selector", click_by="css selector",
    timeout=None, js_click=False)

self.hover_and_js_click(
    hover_selector, click_selector,
    hover_by="css selector", click_by="css selector",
    timeout=None)

self.hover_and_double_click(
    hover_selector, click_selector,
    hover_by="css selector", click_by="css selector",
    timeout=None)

self.drag_and_drop(
    drag_selector, drop_selector,
    drag_by="css selector", drop_by="css selector",
    timeout=None, jquery=False)

self.drag_and_drop_with_offset(
    selector, x, y, by="css selector", timeout=None)

self.select_option_by_text(
    dropdown_selector, option, dropdown_by="css selector", timeout=None)

self.select_option_by_index(
    dropdown_selector, option, dropdown_by="css selector", timeout=None)

self.select_option_by_value(
    dropdown_selector, option, dropdown_by="css selector", timeout=None)

self.get_select_options(
    dropdown_selector, attribute="text", by="css selector", timeout=None)

self.load_html_string(html_string, new_page=True)

self.set_content(html_string, new_page=False)

self.load_html_file(html_file, new_page=True)

self.open_html_file(html_file)

self.execute_script(script, *args, **kwargs)

self.execute_cdp_cmd(script, *args, **kwargs)

self.execute_async_script(script, timeout=None)

self.safe_execute_script(script, *args, **kwargs)

self.get_gui_element_rect(selector, by="css selector")

self.get_gui_element_center(selector, by="css selector")

self.get_window_rect()

self.get_window_size()

self.get_window_position()

self.set_window_rect(x, y, width, height)

self.set_window_size(width, height)

self.set_window_position(x, y)

self.maximize_window()

self.switch_to_frame(frame="iframe", timeout=None)

self.switch_to_default_content()

self.switch_to_parent_frame()

with self.frame_switch(frame, timeout=None):
    # Indented Code Block for Context Manager (Must use "with")

self.set_content_to_frame(frame, timeout=None)

self.set_content_to_default(nested=False)
# Duplicates: self.set_content_to_default_content(nested=False)

self.set_content_to_parent()
# Duplicates: self.set_content_to_parent_frame()

self.open_new_window(switch_to=True)
# Duplicates: self.open_new_tab(switch_to=True)

self.switch_to_window(window, timeout=None)
# Duplicates: self.switch_to_tab(tab, timeout=None)

self.switch_to_default_window()
# Duplicates: self.switch_to_default_tab()

self.switch_to_newest_window()
# Duplicates: self.switch_to_newest_tab()

self.get_new_driver(
    browser=None,
    headless=None,
    locale_code=None,
    protocol=None,
    servername=None,
    port=None,
    proxy=None,
    proxy_bypass_list=None,
    proxy_pac_url=None,
    multi_proxy=None,
    agent=None,
    switch_to=True,
    cap_file=None,
    cap_string=None,
    recorder_ext=None,
    disable_cookies=None,
    disable_js=None,
    disable_csp=None,
    enable_ws=None,
    enable_sync=None,
    use_auto_ext=None,
    undetectable=None,
    uc_cdp_events=None,
    uc_subprocess=None,
    log_cdp_events=None,
    no_sandbox=None,
    disable_gpu=None,
    headless1=None,
    headless2=None,
    incognito=None,
    guest_mode=None,
    dark_mode=None,
    devtools=None,
    remote_debug=None,
    enable_3d_apis=None,
    swiftshader=None,
    ad_block_on=None,
    host_resolver_rules=None,
    block_images=None,
    do_not_track=None,
    chromium_arg=None,
    firefox_arg=None,
    firefox_pref=None,
    user_data_dir=None,
    extension_zip=None,
    extension_dir=None,
    disable_features=None,
    binary_location=None,
    driver_version=None,
    page_load_strategy=None,
    use_wire=None,
    external_pdf=None,
    is_mobile=None,
    d_width=None,
    d_height=None,
    d_p_r=None,
)

self.switch_to_driver(driver)

self.switch_to_default_driver()

self.save_screenshot(name, folder=None, selector=None, by="css selector")

self.save_screenshot_to_logs(name=None, selector=None, by="css selector")

self.save_data_to_logs(data, file_name=None)

self.append_data_to_logs(data, file_name=None)

self.save_page_source(name, folder=None)

self.save_cookies(name="cookies.txt")

self.load_cookies(name="cookies.txt", expiry=False)

self.delete_all_cookies()
# Duplicates: self.clear_all_cookies()

self.delete_saved_cookies(name="cookies.txt")

self.get_saved_cookies(name="cookies.txt")

self.get_cookie(name)

self.get_cookies()

self.add_cookie(cookie_dict, expiry=False)

self.add_cookies(cookies, expiry=False)

self.wait_for_ready_state_complete(timeout=None)

self.wait_for_angularjs(timeout=None)

self.sleep(seconds)
# Duplicates: self.wait(seconds)

self.install_addon(xpi_file)

self.activate_jquery()

self.activate_demo_mode()

self.deactivate_demo_mode()

self.activate_design_mode()

self.deactivate_design_mode()

self.activate_recorder()

self.save_recorded_actions()

self.bring_active_window_to_front()

self.bring_to_front(selector, by="css selector")

self.highlight_click(selector, by="css selector", loops=3, scroll=True, timeout=None)

self.highlight_type(selector, text, by="css selector", loops=3, scroll=True, timeout=None)
# Duplicates:
# self.highlight_update_text(
#     selector, text, by="css selector", loops=3, scroll=True, timeout=None)

self.highlight_if_visible(selector, by="css selector", loops=4, scroll=True)

self.highlight(selector, by="css selector", loops=4, scroll=True, timeout=None)

self.highlight_elements(selector, by="css selector", loops=4, scroll=True, limit=0)

self.press_up_arrow(selector="html", times=1, by="css selector")

self.press_down_arrow(selector="html", times=1, by="css selector")

self.press_left_arrow(selector="html", times=1, by="css selector")

self.press_right_arrow(selector="html", times=1, by="css selector")

self.scroll_to(selector, by="css selector", timeout=None)
# Duplicates: self.scroll_to_element(selector, by="css selector")

self.slow_scroll_to(selector, by="css selector", timeout=None)
# Duplicates: self.slow_scroll_to_element(selector, by="css selector")

self.scroll_into_view(selector, by="css selector", timeout=None)

self.scroll_to_top()

self.scroll_to_bottom()

self.click_xpath(xpath)

self.js_click(selector, by="css selector", all_matches=False, timeout=None, scroll=True)

self.js_click_if_present(selector, by="css selector", timeout=0)

self.js_click_if_visible(selector, by="css selector", timeout=0)

self.js_click_all(selector, by="css selector", timeout=None)

self.jquery_click(selector, by="css selector", timeout=None)

self.jquery_click_all(selector, by="css selector", timeout=None)

self.hide_element(selector, by="css selector")

self.hide_elements(selector, by="css selector")

self.show_element(selector, by="css selector")

self.show_elements(selector, by="css selector")

self.remove_element(selector, by="css selector")

self.remove_elements(selector, by="css selector")

self.ad_block()
# Duplicates: self.block_ads()

self.show_file_choosers()

self.disable_beforeunload()

self.get_domain_url(url)

self.get_active_element_css()

self.get_beautiful_soup(source=None)

self.get_unique_links()

self.get_link_status_code(link, allow_redirects=False, timeout=5, verify=False)

self.assert_link_status_code_is_not_404(link)

self.assert_no_404_errors(multithreaded=True, timeout=None)
# Duplicates:
# self.assert_no_broken_links(multithreaded=True, timeout=None)

self.print_unique_links_with_status_codes()

self.get_pdf_text(
    pdf, page=None, maxpages=None, password=None,
    codec='utf-8', wrap=False, nav=False, override=False, caching=True)

self.assert_pdf_text(
    pdf, text, page=None, maxpages=None, password=None,
    codec='utf-8', wrap=True, nav=False, override=False, caching=True)

self.create_folder(folder)

self.choose_file(selector, file_path, by="css selector", timeout=None)

self.save_element_as_image_file(selector, file_name, folder=None, overlay_text="")

self.download_file(file_url, destination_folder=None)

self.save_file_as(file_url, new_file_name, destination_folder=None)

self.save_data_as(data, file_name, destination_folder=None)

self.append_data_to_file(data, file_name, destination_folder=None)

self.get_file_data(file_name, folder=None)

self.get_downloads_folder()

self.get_browser_downloads_folder()

self.get_downloaded_files(regex=None, browser=False)

self.get_path_of_downloaded_file(file, browser=False)

self.get_data_from_downloaded_file(file, timeout=None, browser=False)

self.is_downloaded_file_present(file, browser=False)

self.is_downloaded_file_regex_present(regex, browser=False)

self.delete_downloaded_file_if_present(file, browser=False)
# Duplicates: self.delete_downloaded_file(file, browser=False)

self.assert_downloaded_file(file, timeout=None, browser=False)

self.assert_downloaded_file_regex(regex, timeout=None, browser=False)

self.assert_data_in_downloaded_file(data, file, timeout=None, browser=False)

self.assert_true(expr, msg=None)

self.assert_false(expr, msg=None)

self.assert_equal(first, second, msg=None)

self.assert_not_equal(first, second, msg=None)

self.assert_in(first, second, msg=None)

self.assert_not_in(first, second, msg=None)

self.assert_raises(*args, **kwargs)

self.wait_for_attribute(selector, attribute, value=None, by="css selector", timeout=None)

self.assert_attribute(selector, attribute, value=None, by="css selector", timeout=None)

self.assert_title(title)

self.assert_title_contains(substring)

self.assert_url(url)

self.assert_url_contains(substring)

self.assert_no_js_errors(exclude=[])

self.inspect_html()

self.is_valid_url(url)

self.is_alert_present()

self.is_online()

self.is_chromium()

self.get_chrome_version()

self.get_chromium_version()

self.get_chromedriver_version()

self.get_chromium_driver_version()

self.get_mfa_code(totp_key=None)
# Duplicates:
# self.get_totp_code(totp_key=None)
# self.get_google_auth_password(totp_key=None)
# self.get_google_auth_code(totp_key=None)

self.enter_mfa_code(selector, totp_key=None, by="css selector", timeout=None)
# Duplicates:
# self.enter_totp_code(selector, totp_key=None, by="css selector", timeout=None)

self.convert_css_to_xpath(css)

self.convert_xpath_to_css(xpath)

self.convert_to_css_selector(selector, by)

self.set_value(selector, text, by="css selector", timeout=None, scroll=True)

self.js_update_text(selector, text, by="css selector", timeout=None)
# Duplicates:
# self.js_type(selector, text, by="css selector", timeout=None)
# self.set_text(selector, text, by="css selector", timeout=None)

self.set_text_content(selector, text, by="css selector", timeout=None, scroll=False)

self.jquery_update_text(selector, text, by="css selector", timeout=None)
# Duplicates:
# self.jquery_type(selector, text, by="css selector", timeout=None)

self.get_value(selector, by="css selector", timeout=None)

self.set_time_limit(time_limit)

self.set_default_timeout(timeout)

self.reset_default_timeout()

self.fail(msg=None)

self.skip(reason="")

############

self.start_recording_console_logs()

self.console_log_string(string)

self.console_log_script(script)

self.get_recorded_console_logs()

############

self.set_local_storage_item(key, value)

self.get_local_storage_item(key)

self.remove_local_storage_item(key)

self.clear_local_storage()
# Duplicates: delete_local_storage()

self.get_local_storage_keys()

self.get_local_storage_items()

self.set_session_storage_item(key, value)

self.get_session_storage_item(key)

self.remove_session_storage_item(key)

self.clear_session_storage()
# Duplicates: delete_session_storage()

self.get_session_storage_keys()

self.get_session_storage_items()

############

self.set_wire_proxy(string)  # Requires "--wire"!

############

self.add_css_link(css_link)

self.add_js_link(js_link)

self.add_css_style(css_style)

self.add_js_code_from_link(js_link)

self.add_js_code(js_code)

self.add_meta_tag(http_equiv=None, content=None)

############

self.create_presentation(name=None, theme="default", transition="default")

self.add_slide(
    content=None, image=None, code=None, iframe=None,
    content2=None, notes=None, transition=None, name=None)

self.save_presentation(name=None, filename=None, show_notes=False, interval=0)

self.begin_presentation(name=None, filename=None, show_notes=False, interval=0)

############

self.create_pie_chart(
    chart_name=None, title=None, subtitle=None,
    data_name=None, unit=None, libs=True,
    labels=True, legend=True)

self.create_bar_chart(
    chart_name=None, title=None, subtitle=None,
    data_name=None, unit=None, libs=True,
    labels=True, legend=True)

self.create_column_chart(
    chart_name=None, title=None, subtitle=None,
    data_name=None, unit=None, libs=True,
    labels=True, legend=True)

self.create_line_chart(
    chart_name=None, title=None, subtitle=None,
    data_name=None, unit=None, zero=False, libs=True,
    labels=True, legend=True)

self.create_area_chart(
    chart_name=None, title=None, subtitle=None,
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

self.set_introjs_colors(theme_color=None, hover_color=None)

self.add_tour_step(message, selector=None, name=None, title=None, theme=None, alignment=None)

self.play_tour(name=None, interval=0)
# Duplicates:
# self.start_tour(name=None, interval=0):

self.export_tour(name=None, filename="my_tour.js", url=None)

############

self.activate_jquery_confirm()

self.set_jqc_theme(theme, color=None, width=None)

self.reset_jqc_theme()

self.get_jqc_button_input(message, buttons, options=None)

self.get_jqc_text_input(message, button=None, options=None)

self.get_jqc_form_inputs(message, buttons, options=None)

############

self.activate_messenger()

self.post_message(message, duration=None, pause=True, style="info")

self.post_message_and_highlight(message, selector, by="css selector")

self.post_success_message(message, duration=None, pause=True)

self.post_error_message(message, duration=None, pause=True)

self.set_messenger_theme(theme="default", location="default", max_messages="default")

############

self.generate_referral(start_page, destination_page, selector=None)

self.generate_traffic(start_page, destination_page, loops=1, selector=None)

self.generate_referral_chain(pages)

self.generate_traffic_chain(pages, loops=1)

############

self.get_element(selector, by="css selector", timeout=None)
# Duplicates:
# self.wait_for_selector(selector, by="css selector", timeout=None)
# self.locator(selector, by="css selector", timeout=None)
# self.wait_for_element_present(selector, by="css selector", timeout=None)

self.wait_for_query_selector(selector, by="css selector", timeout=None)

self.assert_element_present(selector, by="css selector", timeout=None)

self.assert_elements_present(*args, **kwargs)

############

self.find_element(selector, by="css selector", timeout=None)
# Duplicates:
# self.wait_for_element(selector, by="css selector", timeout=None)
# self.wait_for_element_visible(selector, by="css selector", timeout=None)

self.assert_element(selector, by="css selector", timeout=None)
# Duplicates:
# self.assert_element_visible(selector, by="css selector", timeout=None)

self.assert_elements(*args, **kwargs)
# Duplicates:
# self.assert_elements_visible(*args, **kwargs)

############

self.find_text(text, selector="html", by="css selector", timeout=None)
# Duplicates:
# self.wait_for_text(text, selector="html", by="css selector", timeout=None)
# self.wait_for_text_visible(text, selector="html", by="css selector", timeout=None)

self.find_exact_text(text, selector="html", by="css selector", timeout=None)
# Duplicates:
# self.wait_for_exact_text(text, selector="html", by="css selector", timeout=None)
# self.wait_for_exact_text_visible(text, selector="html", by="css selector", timeout=None)

self.find_non_empty_text(selector="html", by="css selector", timeout=None)
# Duplicates:
# self.wait_for_non_empty_text(selector="html", by="css selector", timeout=None)
# self.wait_for_non_empty_text_visible(selector="html", by="css selector", timeout=None)

self.assert_text(text, selector="html", by="css selector", timeout=None)
# Duplicates:
# self.assert_text_visible(text, selector="html", by="css selector", timeout=None)

self.assert_exact_text(text, selector="html", by="css selector", timeout=None)

############

self.wait_for_link_text_present(link_text, timeout=None)

self.wait_for_partial_link_text_present(link_text, timeout=None)

self.find_link_text(link_text, timeout=None)
# Duplicates:
# self.wait_for_link_text(link_text, timeout=None)
# self.wait_for_link_text_visible(link_text, timeout=None)

self.assert_link_text(link_text, timeout=None)
# Duplicates:
# self.assert_link(link_text, timeout=None)

############

self.find_partial_link_text(partial_link_text, timeout=None)
# Duplicates:
# self.wait_for_partial_link_text(partial_link_text, timeout=None)

self.assert_partial_link_text(partial_link_text, timeout=None)

############

self.wait_for_element_absent(selector, by="css selector", timeout=None)
# Duplicates:
# self.wait_for_element_not_present(selector, by="css selector", timeout=None)

self.assert_element_absent(selector, by="css selector", timeout=None)
# Duplicates:
# self.assert_element_not_present(selector, by="css selector", timeout=None)

############

self.wait_for_element_clickable(selector, by="css selector", timeout=None)

############

self.wait_for_element_not_visible(selector, by="css selector", timeout=None)

self.assert_element_not_visible(selector, by="css selector", timeout=None)

############

self.wait_for_text_not_visible(text, selector="html", by="css selector", timeout=None)

self.wait_for_exact_text_not_visible(text, selector="html", by="css selector", timeout=None)

self.assert_text_not_visible(text, selector="html", by="css selector", timeout=None)

self.assert_exact_text_not_visible(text, selector="html", by="css selector", timeout=None)

self.assert_non_empty_text(selector="html", by="css selector", timeout=None)

############

self.wait_for_attribute_not_present(
    selector, attribute, value=None, by="css selector", timeout=None)

self.assert_attribute_not_present(
    selector, attribute, value=None, by="css selector", timeout=None)

############

self.accept_alert(timeout=None)
# Duplicates:
# self.wait_for_and_accept_alert(timeout=None)

self.dismiss_alert(timeout=None)
# Duplicates:
# self.wait_for_and_dismiss_alert(timeout=None)

self.switch_to_alert(timeout=None)
# Duplicates:
# self.wait_for_and_switch_to_alert(timeout=None)

############

self.quit_extra_driver(driver=None)

############

self.check_window(name="default", level=0, baseline=False, check_domain=True, full_diff=False)

############

self.deferred_assert_element(selector, by="css selector", timeout=None, fs=False)
# Duplicates:
# self.delayed_assert_element(
#     selector, by="css selector", timeout=None, fs=False)

self.deferred_assert_element_present(selector, by="css selector", timeout=None, fs=False)
# Duplicates:
# self.delayed_assert_element_present(
#     selector, by="css selector", timeout=None, fs=False)

self.deferred_assert_text(text, selector="html", by="css selector", timeout=None, fs=False)
# Duplicates:
# self.delayed_assert_text(
#     text, selector="html", by="css selector", timeout=None, fs=False)

self.deferred_assert_exact_text(
    text, selector="html", by="css selector", timeout=None, fs=False)
# Duplicates:
# self.delayed_assert_exact_text(
#     text, selector="html", by="css selector", timeout=None, fs=False)

self.deferred_assert_non_empty_text(
    selector="html", by="css selector", timeout=None, fs=False)
# Duplicates:
# self.delayed_assert_non_empty_text(
#     selector="html", by="css selector", timeout=None, fs=False)

self.deferred_check_window(
    name="default", level=0, baseline=False, check_domain=True, full_diff=False, fs=False)
# Duplicates:
# self.delayed_check_window(
#     name="default", level=0, baseline=False,
#     check_domain=True, full_diff=False, fs=False)

self.process_deferred_asserts(print_only=False)
# Duplicates: self.process_delayed_asserts(print_only=False)

############

self.fail(msg=None)  # Inherited from "unittest"

self._check_browser()  # Fails test cleanly if the active window is closed

self._print(TEXT)  # Calls Python's print() / Allows for translations

############

# "driver"-specific methods added (or modified) by SeleniumBase

driver.default_get(url)  # Because driver.get(url) works differently in UC Mode

driver.open(url)  # Like driver.get(), but allows partial URLs without protocol

driver.click(selector)

driver.click_link(link_text)

driver.click_if_visible(selector)

driver.click_active_element()

driver.send_keys(selector, text)

driver.press_keys(selector, text)

driver.type(selector, text)

driver.submit(selector)

driver.assert_element(selector)

driver.assert_element_present(selector)

driver.assert_element_not_visible(selector)

driver.assert_text(text, selector)

driver.assert_exact_text(text, selector)

driver.find_element(selector)

driver.find_elements(selector)

driver.wait_for_element(selector)

driver.wait_for_element_visible(selector)

driver.wait_for_element_present(selector)

driver.wait_for_selector(selector)

driver.wait_for_text(text, selector)

driver.wait_for_exact_text(text, selector)

driver.wait_for_and_accept_alert()

driver.wait_for_and_dismiss_alert()

driver.is_element_present(selector)

driver.is_element_visible(selector)

driver.is_text_visible(text, selector)

driver.is_exact_text_visible(text, selector)

driver.is_attribute_present(selector, attribute)

driver.get_text(selector)

driver.js_click(selector)

driver.get_active_element_css()

driver.get_locale_code()

driver.get_origin()

driver.get_user_agent()

driver.highlight(selector)

driver.highlight_click(selector)

driver.highlight_if_visible(selector)

driver.sleep(seconds)

driver.locator(selector)

driver.get_attribute(selector, attribute)

driver.get_page_source()

driver.get_title()

driver.switch_to_frame(frame="iframe")

############

# "driver"-specific methods added (or modified) by SeleniumBase for UC Mode:

driver.get(url)  # If UC Mode and site detects bots, then uc_open_with_tab(url)

driver.uc_open(url)  # (Open in same tab with default reconnect_time)

driver.uc_open_with_tab(url)  # (New tab with default reconnect_time)

driver.uc_open_with_reconnect(url, reconnect_time=None)  # (New tab)

driver.uc_open_with_disconnect(url, timeout=None)  # New tab + sleep()

driver.reconnect(timeout)  # disconnect() + sleep(timeout) + connect()

driver.disconnect()  # Stops the webdriver service to prevent detection

driver.connect()  # Starts the webdriver service to allow actions again

driver.uc_click(selector)  # A stealthy click for evading bot-detection

driver.uc_gui_press_key(key)  # Use PyAutoGUI to press the keyboard key

driver.uc_gui_press_keys(keys)  # Use PyAutoGUI to press a list of keys

driver.uc_gui_write(text)  # Similar to uc_gui_press_keys(), but faster

driver.uc_gui_click_x_y(x, y, timeframe=0.25)  # PyAutoGUI click screen

driver.uc_gui_click_captcha(frame="iframe", retry=False, blind=False)
# driver.uc_gui_click_cf(frame="iframe", retry=False, blind=False)
# driver.uc_gui_click_rc(frame="iframe", retry=False, blind=False)

driver.uc_gui_handle_captcha(frame="iframe")  # (Auto-detects the CAPTCHA)
# driver.uc_gui_handle_cf(frame="iframe")  # PyAutoGUI click CF Turnstile
# driver.uc_gui_handle_rc(frame="iframe")  # PyAutoGUI click G. reCAPTCHA
```

--------

<h2>🔵 Examples</h2>

✅ Test Folder: [SeleniumBase/examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)

* [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py)
* [test_demo_site.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py)
* [test_coffee_cart.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_coffee_cart.py)
* [coffee_cart_tests.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/coffee_cart_tests.py)
* [parameterized_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/parameterized_test.py)
* [test_deferred_asserts.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_deferred_asserts.py)
* [test_error_page.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_error_page.py)
* [test_login.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_login.py)
* [test_markers.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_markers.py)
* [test_swag_labs.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py)
* [test_simple_login.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_simple_login.py)
* [test_suite.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_suite.py)
* [test_tinymce.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_tinymce.py)
* And many more...

[<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" title="SeleniumBase" align="center" width="280">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
