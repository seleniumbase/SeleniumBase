### SeleniumBase method summary

Here's a summary of SeleniumBase method definitions, which are defined in [base_case.py](https://github.com/mdmintz/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py)

In order to maintain backwards compatibility with scripts using earlier verions of SeleniumBase, some methods that had their names shortened can also be called by their original method name. *(Ex: wait_for_element_visible was later shortened to wait_for_element and then to find_element, but the longer method names remained to keep older scripts from failing.)*

```python
self.open(url)

self.open_url(url)

self.click(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.click_chain(selectors_list, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT, spacing=0)

self.click_link_text(link_text, timeout=settings.SMALL_TIMEOUT)

self.get_text(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.get_attribute(selector, attribute, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.add_text(selector, new_value, timeout=settings.SMALL_TIMEOUT)

self.send_keys(selector, new_value, timeout=settings.SMALL_TIMEOUT)

self.update_text_value(selector, new_value,
    timeout=settings.SMALL_TIMEOUT, retry=False)

self.update_text(selector, new_value, timeout=settings.SMALL_TIMEOUT,
    retry=False)

self.is_element_present(selector, by=By.CSS_SELECTOR)

self.is_element_visible(selector, by=By.CSS_SELECTOR)

self.is_link_text_visible(link_text)

self.is_text_visible(text, selector, by=By.CSS_SELECTOR)

self.find_visible_elements(selector, by=By.CSS_SELECTOR)

self.execute_script(script)

self.set_window_size(width, height)

self.maximize_window()

self.activate_jquery()

self.scroll_to(selector, by=By.CSS_SELECTOR)

self.slow_scroll_to(selector, by=By.CSS_SELECTOR)

self.scroll_click(selector, by=By.CSS_SELECTOR)

self.jquery_click(selector, by=By.CSS_SELECTOR)

self.jq_format(code)

self.get_domain_url(url)

self.convert_xpath_to_css(xpath)

self.convert_to_css_selector(selector, by)

self.set_value(selector, value, by=By.CSS_SELECTOR)

self.jquery_update_text_value(selector, new_value, by=By.CSS_SELECTOR
    timeout=settings.SMALL_TIMEOUT)

self.jquery_update_text(selector, new_value, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

self.hover_on_element(selector)

self.hover_and_click(hover_selector, click_selector,
    hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT)

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

self.save_screenshot(name, folder=None)
```