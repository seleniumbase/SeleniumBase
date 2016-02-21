### SeleniumBase method summary

Here's a summary of SeleniumBase method definitions, which are defined in [base_case.py](https://github.com/mdmintz/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py)

In order to maintain backwards compatibility with scripts using earlier verions of SeleniumBase, methods of method names that were shortened have also retained their earlier names. *(Ex: wait_for_element_visible was later shortened to wait_for_element, but to keep scripts from failing that still use the longer version, that longer version remained.)*

```python
self.open(url)

self.open_url(url)

self.click(selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.click_chain(selectors_list, by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT, spacing=0)

self.click_link_text(link_text, timeout=settings.SMALL_TIMEOUT)

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

self.scroll_to(selector, wait=True)

self.scroll_click(selector)

self.jquery_click(selector, wait=False)

self.jq_format(code)

self.set_value(selector, value, wait=False)

self.jquery_update_text_value(selector, new_value,
    timeout=settings.SMALL_TIMEOUT)

self.jquery_update_text(selector, new_value,
    timeout=settings.SMALL_TIMEOUT)

self.hover_on_element(selector)

self.hover_and_click(hover_selector, click_selector,
    click_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)

self.wait_for_element_present(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_element_visible(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_element(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_text_visible(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_text(text, selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_link_text_visible(link_text,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_link_text(link_text, timeout=settings.LARGE_TIMEOUT)

self.wait_for_element_absent(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_element_not_visible(selector, by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT)

self.wait_for_ready_state_complete(timeout=settings.EXTREME_TIMEOUT)

self.wait_for_and_accept_alert(timeout=settings.LARGE_TIMEOUT)

self.wait_for_and_dismiss_alert(timeout=settings.LARGE_TIMEOUT)

self.wait_for_and_switch_to_alert(timeout=settings.LARGE_TIMEOUT)

self.save_screenshot(name, folder=None)
```