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

self.click_link_text(link_text, timeout=settings.SMALL_TIMEOUT)

self.click_partial_link_text(partial_link_text, timeout=settings.SMALL_TIMEOUT)

self.get_text(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.get_attribute(selector, attribute, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.refresh_page()

self.get_current_url()

self.get_page_source()

self.get_page_title()

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

self.is_text_visible(text, selector, by=By.CSS_SELECTOR)

self.find_visible_elements(selector, by=By.CSS_SELECTOR)

self.execute_script(script)

self.set_window_size(width, height)

self.maximize_window()

self.activate_jquery()

self.highlight(selector, by=By.CSS_SELECTOR, loops=4, scroll=True)

self.scroll_to(selector, by=By.CSS_SELECTOR)

self.slow_scroll_to(selector, by=By.CSS_SELECTOR)

self.scroll_click(selector, by=By.CSS_SELECTOR)  # DEPRECATED

self.click_xpath(xpath)

self.jquery_click(selector, by=By.CSS_SELECTOR)

self.jq_format(code)

self.get_domain_url(url)

self.download_file(file_url, destination_folder=None)

self.save_file_as(file_url, new_file_name, destination_folder=None)

self.convert_xpath_to_css(xpath)

self.convert_to_css_selector(selector, by)

self.set_value(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.jquery_update_text_value(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.jquery_update_text(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.hover_on_element(selector)

self.hover_and_click(hover_selector, click_selector,
    hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.pick_select_option_by_text(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.pick_select_option_by_index(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.pick_select_option_by_value(dropdown_selector, option,
    dropdown_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

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

########

self.wait_for_text_visible(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_text(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.find_text(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.assert_text(text, selector, by=By.CSS_SELECTOR,
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

self.switch_to_window(window, timeout=settings.SMALL_TIMEOUT)

self.switch_to_default_content()

self.save_screenshot(name, folder=None)

########

self.check_assert_element(selector, by=By.CSS_SELECTOR,
    timeout=settings.TINY_TIMEOUT)

self.check_assert_text(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.TINY_TIMEOUT)

self.process_checks()
```