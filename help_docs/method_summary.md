### SeleniumBase method summary

Here's a summary of SeleniumBase method definitions, which are defined in [base_case.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py)

In order to maintain backwards compatibility with scripts using earlier verions of SeleniumBase, some methods that had their names shortened can also be called by their original method name. *(Ex: wait_for_element_visible was later shortened to wait_for_element and then to find_element, but the longer method names remained to keep older scripts from failing.)*

```python
self.open(url)

self.open_url(url)

self.click(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.double_click(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.click_chain(selectors_list, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT, spacing=0)

self.is_link_text_present(link_text)

self.get_link_attribute(link_text, attribute, hard_fail)

self.wait_for_link_text_present(link_text, timeout=settings.SMALL_TIMEOUT)

self.click_link_text(link_text, timeout=settings.SMALL_TIMEOUT)

self.click_link(link_text, timeout=settings.SMALL_TIMEOUT)

self.click_partial_link_text(partial_link_text, timeout=settings.SMALL_TIMEOUT)

self.get_text(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.get_attribute(selector, attribute, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.set_attribute(selector, attribute, value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.remove_attribute(selector, attribute, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.get_property_value(selector, property, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.refresh_page()

self.refresh()

self.get_current_url()

self.get_page_source()

self.get_page_title()

self.get_title()

self.go_back()

self.go_forward()

self.get_image_url(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.add_text(selector, new_value, timeout=settings.SMALL_TIMEOUT)

self.send_keys(selector, new_value, timeout=settings.SMALL_TIMEOUT)

self.update_text_value(selector, new_value,
    timeout=settings.SMALL_TIMEOUT, retry=False)

self.update_text(selector, new_value, timeout=settings.SMALL_TIMEOUT,
    retry=False)

self.is_element_present(selector, by=By.CSS_SELECTOR)

self.is_element_visible(selector, by=By.CSS_SELECTOR)

self.is_link_text_visible(link_text)

self.is_partial_link_text_visible(partial_link_text)

self.is_text_visible(text, selector="html", by=By.CSS_SELECTOR)

self.find_elements(selector, by=By.CSS_SELECTOR, limit=0)

self.find_visible_elements(selector, by=By.CSS_SELECTOR, limit=0)

self.click_visible_elements(selector, by=By.CSS_SELECTOR, limit=0)

self.is_element_in_an_iframe(selector, by=By.CSS_SELECTOR)

self.switch_to_frame_of_element(selector, by=By.CSS_SELECTOR)

self.execute_script(script)

self.set_window_size(width, height)

self.maximize_window()

self.add_css_link(css_link)

self.add_js_link(js_link)

self.add_css_style(css_style)

self.add_js_code_from_link(js_link)

self.add_meta_tag(http_equiv=None, content=None)

self.activate_jquery()

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

self.post_success_message(message, duration=None, pause=True)

self.post_error_message(message, duration=None, pause=True)

self.set_messenger_theme(theme="default", location="default",
    max_messages="default")

self.bring_to_front(selector, by=By.CSS_SELECTOR)

self.highlight(selector, by=By.CSS_SELECTOR, loops=4, scroll=True)

self.scroll_to(selector, by=By.CSS_SELECTOR)

self.slow_scroll_to(selector, by=By.CSS_SELECTOR)

self.click_xpath(xpath)

self.js_click(selector, by=By.CSS_SELECTOR)

self.jquery_click(selector, by=By.CSS_SELECTOR)

self.submit(selector, by=By.CSS_SELECTOR)

self.hide_element(selector, by=By.CSS_SELECTOR)

self.hide_elements(selector, by=By.CSS_SELECTOR)

self.show_element(selector, by=By.CSS_SELECTOR)

self.show_elements(selector, by=By.CSS_SELECTOR)

self.remove_element(selector, by=By.CSS_SELECTOR)

self.remove_elements(selector, by=By.CSS_SELECTOR)

self.ad_block()

self.get_domain_url(url)

self.get_beautiful_soup(source=None)

self.get_unique_links()

self.get_link_status_code(link, allow_redirects=False, timeout=5)

self.assert_link_status_code_is_not_404(link)

self.assert_no_404_errors(multithreaded=True)

self.print_unique_links_with_status_codes()

self.safe_execute_script(script)

self.create_folder(folder)

self.save_element_as_image_file(selector, file_name, folder=None)

self.download_file(file_url, destination_folder=None)

self.save_file_as(file_url, new_file_name, destination_folder=None)

self.save_data_as(data, file_name, destination_folder=None)

self.get_downloads_folder(file)

self.get_path_of_downloaded_file(file)

self.is_downloaded_file_present(file)

self.assert_downloaded_file(file)

self.assert_true(expr, msg=None)

self.assert_false(expr, msg=None)

self.assert_equal(first, second, msg=None)

self.assert_not_equal(first, second, msg=None)

self.assert_no_js_errors()

self.get_google_auth_password(totp_key=None)

self.convert_xpath_to_css(xpath)

self.convert_to_css_selector(selector, by)

self.set_value(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.js_update_text(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.jquery_update_text_value(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.jquery_update_text(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.hover_on_element(selector, by=By.CSS_SELECTOR)

self.hover_and_click(hover_selector, click_selector,
    hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.select_option_by_text(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.select_option_by_index(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.select_option_by_value(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

########

self.generate_referral(start_page, destination_page)

self.generate_traffic(start_page, destination_page, loops=1)

self.generate_referral_chain(pages)

self.generate_traffic_chain(pages, loops=1)

########

self.wait_for_element_present(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.assert_element_present(selector, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_element_visible(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_element(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.find_element(selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT)

self.assert_element(
    selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.assert_element_visible(
    selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_text_visible(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_exact_text_visible(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_text(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.find_text(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.assert_text_visible(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.assert_text(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.assert_exact_text(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_link_text_visible(link_text, timeout=settings.LARGE_TIMEOUT)

self.wait_for_link_text(link_text, timeout=settings.LARGE_TIMEOUT)

self.find_link_text(link_text, timeout=settings.LARGE_TIMEOUT)

self.assert_link_text(link_text, timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_partial_link_text(partial_link_text,
    timeout=settings.LARGE_TIMEOUT)

self.find_partial_link_text(partial_link_text,
    timeout=settings.LARGE_TIMEOUT)

self.assert_partial_link_text(partial_link_text,
    timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_element_absent(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.assert_element_absent(selector, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_element_not_visible(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.assert_element_not_visible(selector, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

########

self.wait_for_ready_state_complete(timeout=settings.EXTREME_TIMEOUT)

self.wait_for_and_accept_alert(timeout=settings.LARGE_TIMEOUT)

self.wait_for_and_dismiss_alert(timeout=settings.LARGE_TIMEOUT)

self.wait_for_and_switch_to_alert(timeout=settings.LARGE_TIMEOUT)

self.switch_to_frame(frame, timeout=settings.SMALL_TIMEOUT)

self.switch_to_default_content()

self.open_new_window(switch_to=True)

self.switch_to_window(window, timeout=settings.SMALL_TIMEOUT)

self.switch_to_default_window()

self.check_window(name="default", level=0, baseline=False)

self.save_screenshot(name, folder=None)

self.get_new_driver(browser=None, headless=None, servername=None, port=None,
                    proxy=None, switch_to=True, cap_file=None)

self.switch_to_driver(driver)

self.switch_to_default_driver()

########

self.delayed_assert_element(selector, by=By.CSS_SELECTOR,
    timeout=settings.MINI_TIMEOUT)

self.delayed_assert_text(text, selector="html", by=By.CSS_SELECTOR,
    timeout=settings.MINI_TIMEOUT)

self.process_delayed_asserts()
```

---

Example Test: (<i>From [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py)</i>)

![](https://cdn2.hubspot.net/hubfs/100006/images/SampleCode2.png "SeleniumBase Python Code")
