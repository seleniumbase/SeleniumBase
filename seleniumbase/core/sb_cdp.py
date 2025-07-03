"""Add CDP methods to extend the driver"""
import asyncio
import fasteners
import os
import re
import sys
import time
from contextlib import suppress
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import shared_utils
from seleniumbase.undetected.cdp_driver import cdp_util


class CDPMethods():
    def __init__(self, loop, page, driver):
        self.loop = loop
        self.page = page
        self.driver = driver

    def _swap_driver(self, driver):
        self.driver = driver
        self.page = driver.cdp.page
        self.loop = driver.cdp.loop

    def __slow_mode_pause_if_set(self):
        if (
            (hasattr(sb_config, "demo_mode") and sb_config.demo_mode)
            or "--demo" in sys.argv
        ):
            time.sleep(0.48)
        elif (
            (hasattr(sb_config, "slow_mode") and sb_config.slow_mode)
            or "--slow" in sys.argv
        ):
            time.sleep(0.24)

    def __add_light_pause(self):
        time.sleep(0.007)

    def __convert_to_css_if_xpath(self, selector):
        if page_utils.is_xpath_selector(selector):
            with suppress(Exception):
                css = js_utils.convert_to_css_selector(selector, "xpath")
                if css:
                    return css
        return selector

    def __add_sync_methods(self, element):
        if not element:
            return element
        element.clear_input = lambda: self.__clear_input(element)
        element.click = lambda: self.__click(element)
        element.flash = lambda *args, **kwargs: self.__flash(
            element, *args, **kwargs
        )
        element.focus = lambda: self.__focus(element)
        element.gui_click = (
            lambda *args, **kwargs: self.__gui_click(element, *args, **kwargs)
        )
        element.highlight_overlay = lambda: self.__highlight_overlay(element)
        element.mouse_click = lambda: self.__mouse_click(element)
        element.mouse_drag = (
            lambda destination: self.__mouse_drag(element, destination)
        )
        element.mouse_move = lambda: self.__mouse_move(element)
        element.press_keys = lambda text: self.__press_keys(element, text)
        element.query_selector = (
            lambda selector: self.__query_selector(element, selector)
        )
        element.querySelector = element.query_selector
        element.query_selector_all = (
            lambda selector: self.__query_selector_all(element, selector)
        )
        element.querySelectorAll = element.query_selector_all
        element.remove_from_dom = lambda: self.__remove_from_dom(element)
        element.save_screenshot = (
            lambda *args, **kwargs: self.__save_screenshot(
                element, *args, **kwargs)
        )
        element.save_to_dom = lambda: self.__save_to_dom(element)
        element.scroll_into_view = lambda: self.__scroll_into_view(element)
        element.select_option = lambda: self.__select_option(element)
        element.send_file = (
            lambda *file_paths: self.__send_file(element, *file_paths)
        )
        element.send_keys = lambda text: self.__send_keys(element, text)
        element.set_text = lambda value: self.__set_text(element, value)
        element.set_value = lambda value: self.__set_value(element, value)
        element.type = lambda text: self.__type(element, text)
        element.get_position = lambda: self.__get_position(element)
        element.get_html = lambda: self.__get_html(element)
        element.get_js_attributes = lambda: self.__get_js_attributes(element)
        element.get_attribute = (
            lambda attribute: self.__get_attribute(element, attribute)
        )
        # element.get_parent() should come last
        element.get_parent = lambda: self.__get_parent(element)
        return element

    def get(self, url, **kwargs):
        url = shared_utils.fix_url_as_needed(url)
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        self.loop.run_until_complete(self.page.get(url, **kwargs))
        url_protocol = url.split(":")[0]
        safe_url = True
        if url_protocol not in ["about", "data", "chrome"]:
            safe_url = False
        if not safe_url:
            time.sleep(constants.UC.CDP_MODE_OPEN_WAIT)
            if shared_utils.is_windows():
                time.sleep(constants.UC.EXTRA_WINDOWS_WAIT)
        else:
            time.sleep(0.012)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def open(self, url, **kwargs):
        self.get(url, **kwargs)

    def reload(self, ignore_cache=True, script_to_evaluate_on_load=None):
        self.loop.run_until_complete(
            self.page.reload(
                ignore_cache=ignore_cache,
                script_to_evaluate_on_load=script_to_evaluate_on_load,
            )
        )

    def refresh(self, *args, **kwargs):
        self.reload(*args, **kwargs)

    def get_event_loop(self):
        return self.loop

    def add_handler(self, event, handler):
        self.page.add_handler(event, handler)

    def find_element(self, selector, best_match=False, timeout=None):
        """Similar to select(), but also finds elements by text content.
        When using text-based searches, if best_match=False, then will
        find the first element with the text. If best_match=True, then
        if multiple elements have that text, then will use the element
        with the closest text-length to the text being searched for."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        early_failure = False
        if (":contains(") in selector:
            selector, _ = page_utils.recalculate_selector(
                selector, by="css selector", xp_ok=True
            )
        failure = False
        try:
            if early_failure:
                raise Exception("Failed!")
            element = self.loop.run_until_complete(
                self.page.find(
                    selector, best_match=best_match, timeout=timeout
                )
            )
        except Exception:
            failure = True
            plural = "s"
            if timeout == 1:
                plural = ""
            message = "\n Element {%s} was not found after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
        if failure:
            raise Exception(message)
        element = self.__add_sync_methods(element)
        self.__slow_mode_pause_if_set()
        return element

    def find_element_by_text(self, text, tag_name=None, timeout=None):
        """Returns an element by matching text.
        Optionally, provide a tag_name to narrow down the search to an
        element with the given tag. (Eg: a, button, div, script, span)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__add_light_pause()
        time_now = time.time()
        self.assert_text(text, timeout=timeout)
        spent = int(time.time() - time_now)
        remaining = 1 + timeout - spent
        if tag_name:
            self.assert_element(tag_name, timeout=remaining)
        elements = self.loop.run_until_complete(
            self.page.find_elements_by_text(text=text)
        )
        if tag_name:
            tag_name = tag_name.lower().strip()
        for element in elements:
            if element and not tag_name:
                element = self.__add_sync_methods(element)
                return self.__add_sync_methods(element)
            elif (
                element
                and tag_name in element.tag_name.lower()
                and text.strip() in element.text
            ):
                element = self.__add_sync_methods(element)
                return self.__add_sync_methods(element)
            elif (
                element
                and element.parent
                and tag_name in element.parent.tag_name.lower()
                and text.strip() in element.parent.text
            ):
                element = self.__add_sync_methods(element.parent)
                return self.__add_sync_methods(element)
            elif (
                element
                and element.parent
                and element.parent.parent
                and tag_name in element.parent.parent.tag_name.lower()
                and text.strip() in element.parent.parent.text
            ):
                element = self.__add_sync_methods(element.parent.parent)
                return self.__add_sync_methods(element)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Text {%s} with tag {%s} was not found after %s second%s!"
            % (text, tag_name, timeout, plural)
        )

    def find_all(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        elements = self.loop.run_until_complete(
            self.page.find_all(selector, timeout=timeout)
        )
        updated_elements = []
        for element in elements:
            element = self.__add_sync_methods(element)
            updated_elements.append(element)
        return updated_elements

    def find_elements_by_text(self, text, tag_name=None):
        """Returns a list of elements by matching text.
        Optionally, provide a tag_name to narrow down the search to only
        elements with the given tag. (Eg: a, button, div, script, span)"""
        self.__add_light_pause()
        elements = self.loop.run_until_complete(
            self.page.find_elements_by_text(text=text)
        )
        updated_elements = []
        if tag_name:
            tag_name = tag_name.lower().strip()
        for element in elements:
            if element and not tag_name:
                element = self.__add_sync_methods(element)
                if element not in updated_elements:
                    updated_elements.append(element)
            elif (
                element
                and tag_name in element.tag_name.lower()
                and text.strip() in element.text
            ):
                element = self.__add_sync_methods(element)
                if element not in updated_elements:
                    updated_elements.append(element)
            elif (
                element
                and element.parent
                and tag_name in element.parent.tag_name.lower()
                and text.strip() in element.parent.text
            ):
                element = self.__add_sync_methods(element.parent)
                if element not in updated_elements:
                    updated_elements.append(element)
            elif (
                element
                and element.parent
                and element.parent.parent
                and tag_name in element.parent.parent.tag_name.lower()
                and text.strip() in element.parent.parent.text
            ):
                element = self.__add_sync_methods(element.parent.parent)
                if element not in updated_elements:
                    updated_elements.append(element)
        return updated_elements

    def select(self, selector, timeout=None):
        """Similar to find_element()."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        if (":contains(" in selector):
            tag_name = selector.split(":contains(")[0].split(" ")[-1]
            text = selector.split(":contains(")[1].split(")")[0][1:-1]
            with suppress(Exception):
                new_timeout = timeout
                if new_timeout < 1:
                    new_timeout = 1
                self.loop.run_until_complete(
                    self.page.select(tag_name, timeout=new_timeout)
                )
                self.loop.run_until_complete(
                    self.page.find(text, timeout=new_timeout)
                )
            elements = self.find_elements_by_text(text, tag_name=tag_name)
            if not elements:
                plural = "s"
                if timeout == 1:
                    plural = ""
                msg = "\n Element {%s} was not found after %s second%s!"
                message = msg % (selector, timeout, plural)
                raise Exception(message)
            element = self.__add_sync_methods(elements[0])
            return element
        failure = False
        try:
            element = self.loop.run_until_complete(
                self.page.select(selector, timeout=timeout)
            )
        except Exception:
            failure = True
            plural = "s"
            if timeout == 1:
                plural = ""
            msg = "\n Element {%s} was not found after %s second%s!"
            message = msg % (selector, timeout, plural)
        if failure:
            raise Exception(message)
        element = self.__add_sync_methods(element)
        self.__slow_mode_pause_if_set()
        return element

    def select_all(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        elements = self.loop.run_until_complete(
            self.page.select_all(selector, timeout=timeout)
        )
        updated_elements = []
        for element in elements:
            element = self.__add_sync_methods(element)
            updated_elements.append(element)
        return updated_elements

    def find_elements(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        return self.select_all(selector, timeout=timeout)

    def find_visible_elements(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        visible_elements = []
        elements = self.select_all(selector, timeout=timeout)
        for element in elements:
            with suppress(Exception):
                position = element.get_position()
                if (position.width != 0 or position.height != 0):
                    visible_elements.append(element)
        return visible_elements

    def click_nth_element(self, selector, number):
        elements = self.select_all(selector)
        if len(elements) < number:
            raise Exception(
                "Not enough matching {%s} elements to "
                "click number %s!" % (selector, number)
            )
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        element.scroll_into_view()
        element.click()

    def click_nth_visible_element(self, selector, number):
        """Finds all matching page elements and clicks the nth visible one.
        Example: self.click_nth_visible_element('[type="checkbox"]', 5)
                (Clicks the 5th visible checkbox on the page.)"""
        elements = self.find_visible_elements(selector)
        if len(elements) < number:
            raise Exception(
                "Not enough matching {%s} elements to "
                "click number %s!" % (selector, number)
            )
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        element.scroll_into_view()
        element.click()

    def click_link(self, link_text):
        self.find_elements_by_text(link_text, "a")[0].click()

    def go_back(self):
        self.loop.run_until_complete(self.page.back())

    def go_forward(self):
        self.loop.run_until_complete(self.page.forward())

    def get_navigation_history(self):
        return self.loop.run_until_complete(self.page.get_navigation_history())

    def __clear_input(self, element):
        return (
            self.loop.run_until_complete(element.clear_input_async())
        )

    def __click(self, element):
        result = (
            self.loop.run_until_complete(element.click_async())
        )
        self.loop.run_until_complete(self.page.wait())
        return result

    def __flash(self, element, *args, **kwargs):
        element.scroll_into_view()
        if len(args) < 3 and "x_offset" not in kwargs:
            x_offset = self.__get_x_scroll_offset()
            kwargs["x_offset"] = x_offset
        if len(args) < 3 and "y_offset" not in kwargs:
            y_offset = self.__get_y_scroll_offset()
            kwargs["y_offset"] = y_offset
        return (
            self.loop.run_until_complete(
                element.flash_async(*args, **kwargs)
            )
        )

    def __focus(self, element):
        return (
            self.loop.run_until_complete(element.focus_async())
        )

    def __gui_click(self, element, timeframe=None):
        element.scroll_into_view()
        self.__add_light_pause()
        position = element.get_position()
        x = position.x
        y = position.y
        e_width = position.width
        e_height = position.height
        # Relative to window
        element_rect = {"height": e_height, "width": e_width, "x": x, "y": y}
        window_rect = self.get_window_rect()
        w_bottom_y = window_rect["y"] + window_rect["height"]
        viewport_height = window_rect["innerHeight"]
        x = window_rect["x"] + element_rect["x"]
        y = w_bottom_y - viewport_height + element_rect["y"]
        y_scroll_offset = window_rect["pageYOffset"]
        y = y - y_scroll_offset
        x = x + window_rect["scrollX"]
        y = y + window_rect["scrollY"]
        # Relative to screen
        element_rect = {"height": e_height, "width": e_width, "x": x, "y": y}
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        x, y = ((e_x + e_width / 2.0) + 0.5), ((e_y + e_height / 2.0) + 0.5)
        if not timeframe or not isinstance(timeframe, (int, float)):
            timeframe = 0.25
        if timeframe > 3:
            timeframe = 3
        self.gui_click_x_y(x, y, timeframe=timeframe)
        return self.loop.run_until_complete(self.page.wait())

    def __highlight_overlay(self, element):
        return (
            self.loop.run_until_complete(element.highlight_overlay_async())
        )

    def __mouse_click(self, element):
        result = (
            self.loop.run_until_complete(element.mouse_click_async())
        )
        self.loop.run_until_complete(self.page.wait())
        return result

    def __mouse_drag(self, element, destination):
        return (
            self.loop.run_until_complete(element.mouse_drag_async(destination))
        )

    def __mouse_move(self, element):
        return (
            self.loop.run_until_complete(element.mouse_move_async())
        )

    def __press_keys(self, element, text):
        element.scroll_into_view()
        submit = False
        if text.endswith("\n") or text.endswith("\r"):
            submit = True
            text = text[:-1]
        for key in text:
            element.send_keys(key)
            time.sleep(0.044)
        if submit:
            element.send_keys("\r\n")
            time.sleep(0.044)
        self.__slow_mode_pause_if_set()
        return self.loop.run_until_complete(self.page.sleep(0.025))

    def __query_selector(self, element, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        element2 = self.loop.run_until_complete(
            element.query_selector_async(selector)
        )
        element2 = self.__add_sync_methods(element2)
        return element2

    def __query_selector_all(self, element, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        elements = self.loop.run_until_complete(
            element.query_selector_all_async(selector)
        )
        updated_elements = []
        for element in elements:
            element = self.__add_sync_methods(element)
            updated_elements.append(element)
        self.__slow_mode_pause_if_set()
        return updated_elements

    def __remove_from_dom(self, element):
        return (
            self.loop.run_until_complete(element.remove_from_dom_async())
        )

    def __save_screenshot(self, element, *args, **kwargs):
        return (
            self.loop.run_until_complete(
                element.save_screenshot_async(*args, **kwargs)
            )
        )

    def __save_to_dom(self, element):
        return (
            self.loop.run_until_complete(element.save_to_dom_async())
        )

    def __scroll_into_view(self, element):
        self.loop.run_until_complete(element.scroll_into_view_async())
        self.__add_light_pause()
        return None

    def __select_option(self, element):
        return (
            self.loop.run_until_complete(element.select_option_async())
        )

    def __send_file(self, element, *file_paths):
        return (
            self.loop.run_until_complete(element.send_file_async(*file_paths))
        )

    def __send_keys(self, element, text):
        return (
            self.loop.run_until_complete(element.send_keys_async(text))
        )

    def __set_text(self, element, value):
        return (
            self.loop.run_until_complete(element.set_text_async(value))
        )

    def __set_value(self, element, value):
        return (
            self.loop.run_until_complete(element.set_value_async(value))
        )

    def __type(self, element, text):
        with suppress(Exception):
            element.clear_input()
        element.send_keys(text)

    def __get_position(self, element):
        return (
            self.loop.run_until_complete(element.get_position_async())
        )

    def __get_html(self, element):
        return (
            self.loop.run_until_complete(element.get_html_async())
        )

    def __get_js_attributes(self, element):
        return (
            self.loop.run_until_complete(element.get_js_attributes_async())
        )

    def __get_attribute(self, element, attribute):
        try:
            return element.get_js_attributes()[attribute]
        except Exception:
            if not attribute:
                raise
            try:
                attribute_str = element.get_js_attributes()
                locate = ' %s="' % attribute
                if locate in attribute_str.outerHTML:
                    outer_html = attribute_str.outerHTML
                    attr_start = outer_html.find(locate) + len(locate)
                    attr_end = outer_html.find('"', attr_start)
                    value = outer_html[attr_start:attr_end]
                    return value
            except Exception:
                pass
        return None

    def __get_parent(self, element):
        return self.__add_sync_methods(element.parent)

    def __get_x_scroll_offset(self):
        x_scroll_offset = self.loop.run_until_complete(
            self.page.evaluate("window.pageXOffset")
        )
        return x_scroll_offset or 0

    def __get_y_scroll_offset(self):
        y_scroll_offset = self.loop.run_until_complete(
            self.page.evaluate("window.pageYOffset")
        )
        return y_scroll_offset or 0

    def tile_windows(self, windows=None, max_columns=0):
        """Tile windows and return the grid of tiled windows."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.tile_windows(windows, max_columns)
        )

    def grant_permissions(self, permissions, origin=None):
        """Grant specific permissions to the current window.
        Applies to all origins if no origin is specified."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.grant_permissions(permissions, origin)
        )

    def grant_all_permissions(self):
        """Grant all permissions to the current window for all origins."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(driver.grant_all_permissions())

    def reset_permissions(self):
        """Reset permissions for all origins on the current window."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(driver.reset_permissions())

    def get_all_cookies(self, *args, **kwargs):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.cookies.get_all(*args, **kwargs)
        )

    def set_all_cookies(self, *args, **kwargs):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.cookies.set_all(*args, **kwargs)
        )

    def save_cookies(self, *args, **kwargs):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.cookies.save(*args, **kwargs)
        )

    def load_cookies(self, *args, **kwargs):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.cookies.load(*args, **kwargs)
        )

    def clear_cookies(self):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(driver.cookies.clear())

    def sleep(self, seconds):
        time.sleep(seconds)

    def bring_active_window_to_front(self):
        self.loop.run_until_complete(self.page.bring_to_front())
        self.__add_light_pause()

    def get_active_element(self):
        return self.loop.run_until_complete(
            self.page.js_dumps("document.activeElement")
        )

    def get_active_element_css(self):
        from seleniumbase.js_code import active_css_js

        js_code = active_css_js.get_active_element_css
        js_code = js_code.replace("return getBestSelector", "getBestSelector")
        return self.loop.run_until_complete(self.page.evaluate(js_code))

    def click(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        element = self.find_element(selector, timeout=timeout)
        element.scroll_into_view()
        element.click()
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def click_active_element(self):
        self.loop.run_until_complete(
            self.page.evaluate("document.activeElement.click()")
        )
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def click_if_visible(self, selector):
        if self.is_element_visible(selector):
            with suppress(Exception):
                element = self.find_element(selector, timeout=0)
                element.scroll_into_view()
                element.click()
                self.__slow_mode_pause_if_set()
                self.loop.run_until_complete(self.page.wait())

    def click_visible_elements(self, selector, limit=0):
        """Finds all matching page elements and clicks visible ones in order.
        If a click reloads or opens a new page, the clicking will stop.
        If no matching elements appear, an Exception will be raised.
        If "limit" is set and > 0, will only click that many elements.
        Also clicks elements that become visible from previous clicks.
        Works best for actions such as clicking all checkboxes on a page.
        Example: self.click_visible_elements('input[type="checkbox"]')"""
        elements = self.select_all(selector)
        click_count = 0
        for element in elements:
            if limit and limit > 0 and click_count >= limit:
                return
            try:
                width = 0
                height = 0
                try:
                    position = element.get_position()
                    width = position.width
                    height = position.height
                except Exception:
                    continue
                if (width != 0 or height != 0):
                    element.scroll_into_view()
                    element.click()
                    click_count += 1
                    time.sleep(0.042)
                    self.__slow_mode_pause_if_set()
                    self.loop.run_until_complete(self.page.wait())
            except Exception:
                break

    def mouse_click(self, selector, timeout=None):
        """(Attempt simulating a mouse click)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        element = self.find_element(selector, timeout=timeout)
        element.scroll_into_view()
        element.mouse_click()
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def nested_click(self, parent_selector, selector):
        """
        Find parent element and click on child element inside it.
        (This can be used to click on elements inside an iframe.)
        """
        element = self.find_element(parent_selector)
        element.query_selector(selector).mouse_click()
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def get_nested_element(self, parent_selector, selector):
        """(Can be used to find an element inside an iframe)"""
        element = self.find_element(parent_selector)
        return element.query_selector(selector)

    def select_option_by_text(self, dropdown_selector, option):
        element = self.find_element(dropdown_selector)
        element.scroll_into_view()
        options = element.query_selector_all("option")
        for found_option in options:
            if found_option.text.strip() == option.strip():
                found_option.select_option()
                return
        raise Exception(
            "Unable to find text option {%s} in dropdown {%s}!"
            % (dropdown_selector, option)
        )

    def flash(
        self,
        selector,  # The CSS Selector to flash
        duration=1,  # (seconds) flash duration
        color="44CC88",  # RGB hex flash color
        pause=0,  # (seconds) If 0, the next action starts during flash
    ):
        """Paint a quickly-vanishing dot over an element."""
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.find_element(selector)
        element.scroll_into_view()
        x_offset = self.__get_x_scroll_offset()
        y_offset = self.__get_y_scroll_offset()
        element.flash(duration, color, x_offset, y_offset)
        if pause and isinstance(pause, (int, float)):
            time.sleep(pause)

    def highlight(self, selector):
        """Highlight an element with multi-colors."""
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.find_element(selector)
        element.scroll_into_view()
        x_offset = self.__get_x_scroll_offset()
        y_offset = self.__get_y_scroll_offset()
        element.flash(0.46, "44CC88", x_offset, y_offset)
        time.sleep(0.15)
        element.flash(0.42, "8844CC", x_offset, y_offset)
        time.sleep(0.15)
        element.flash(0.38, "CC8844", x_offset, y_offset)
        time.sleep(0.15)
        element.flash(0.30, "44CC88", x_offset, y_offset)
        time.sleep(0.30)

    def focus(self, selector):
        element = self.find_element(selector)
        element.scroll_into_view()
        element.focus()

    def highlight_overlay(self, selector):
        self.find_element(selector).highlight_overlay()

    def get_parent(self, element):
        if isinstance(element, str):
            element = self.select(element)
        return self.__add_sync_methods(element.parent)

    def remove_element(self, selector):
        self.select(selector).remove_from_dom()

    def remove_from_dom(self, selector):
        self.select(selector).remove_from_dom()

    def remove_elements(self, selector):
        """Remove all elements on the page that match the selector."""
        css_selector = self.__convert_to_css_if_xpath(selector)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        js_code = (
            """var $elements = document.querySelectorAll('%s');
            var index = 0, length = $elements.length;
            for(; index < length; index++){
            $elements[index].remove();}"""
            % css_selector
        )
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))

    def send_keys(self, selector, text, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        element.scroll_into_view()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def press_keys(self, selector, text, timeout=None):
        """Similar to send_keys(), but presses keys at human speed."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        element.scroll_into_view()
        submit = False
        if text.endswith("\n") or text.endswith("\r"):
            submit = True
            text = text[:-1]
        for key in text:
            element.send_keys(key)
            time.sleep(0.044)
        if submit:
            element.send_keys("\r\n")
            time.sleep(0.044)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def type(self, selector, text, timeout=None):
        """Similar to send_keys(), but clears the text field first."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        element.scroll_into_view()
        with suppress(Exception):
            element.clear_input()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def set_value(self, selector, text, timeout=None):
        """Similar to send_keys(), but clears the text field first."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.__slow_mode_pause_if_set()
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.select(selector, timeout=timeout)
        element.scroll_into_view()
        press_enter = False
        if text.endswith("\n"):
            text = text[:-1]
            press_enter = True
        value = js_utils.escape_quotes_if_needed(re.escape(text))
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        set_value_script = (
            """m_elm = document.querySelector('%s');"""
            """m_elm.value = '%s';""" % (css_selector, value)
        )
        self.loop.run_until_complete(self.page.evaluate(set_value_script))
        the_type = self.get_element_attribute(selector, "type")
        if the_type == "range":
            # Some input sliders need a mouse event to trigger listeners.
            with suppress(Exception):
                mouse_move_script = (
                    """m_elm = document.querySelector('%s');"""
                    """m_evt = new Event('mousemove');"""
                    """m_elm.dispatchEvent(m_evt);""" % css_selector
                )
                self.loop.run_until_complete(
                    self.page.evaluate(mouse_move_script)
                )
        elif press_enter:
            self.__add_light_pause()
            self.send_keys(selector, "\n")
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def submit(self, selector):
        submit_script = (
            """elm = document.querySelector('%s');
            const event = new KeyboardEvent("keydown", {
                key: "Enter",
                keyCode: 13,
                code: "Enter",
                which: 13,
                bubbles: true
            });
            elm.dispatchEvent(event);""" % selector
        )
        self.loop.run_until_complete(self.page.evaluate(submit_script))

    def evaluate(self, expression):
        """Run a JavaScript expression and return the result."""
        expression = expression.strip()
        exp_list = expression.split("\n")
        if exp_list and exp_list[-1].strip().startswith("return "):
            expression = (
                "\n".join(exp_list[0:-1]) + "\n"
                + exp_list[-1].strip()[len("return "):]
            ).strip()
        return self.loop.run_until_complete(self.page.evaluate(expression))

    def js_dumps(self, obj_name):
        """Similar to evaluate(), but for dictionary results."""
        if obj_name.startswith("return "):
            obj_name = obj_name[len("return "):]
        return self.loop.run_until_complete(self.page.js_dumps(obj_name))

    def maximize(self):
        if self.get_window()[1].window_state.value == "maximized":
            return
        elif self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(self.page.maximize())
            time.sleep(0.044)
        return self.loop.run_until_complete(self.page.maximize())

    def minimize(self):
        if self.get_window()[1].window_state.value != "minimized":
            return self.loop.run_until_complete(self.page.minimize())

    def medimize(self):
        if self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(self.page.medimize())
            time.sleep(0.044)
        return self.loop.run_until_complete(self.page.medimize())

    def set_window_rect(self, x, y, width, height):
        if self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(
                self.page.set_window_size(
                    left=x, top=y, width=width, height=height)
            )
            time.sleep(0.044)
        return self.loop.run_until_complete(
            self.page.set_window_size(
                left=x, top=y, width=width, height=height)
        )

    def reset_window_size(self):
        x = settings.WINDOW_START_X
        y = settings.WINDOW_START_Y
        width = settings.CHROME_START_WIDTH
        height = settings.CHROME_START_HEIGHT
        self.set_window_rect(x, y, width, height)
        self.__add_light_pause()

    def open_new_window(self, url=None, switch_to=True):
        return self.open_new_tab(url=url, switch_to=switch_to)

    def switch_to_window(self, window):
        self.switch_to_tab(window)

    def switch_to_newest_window(self):
        self.switch_to_tab(-1)

    def open_new_tab(self, url=None, switch_to=True):
        if not isinstance(url, str):
            url = "about:blank"
        self.loop.run_until_complete(self.page.get(url, new_tab=True))
        if switch_to:
            self.switch_to_newest_tab()

    def switch_to_tab(self, tab):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        if isinstance(tab, int):
            self.page = driver.tabs[tab]
        elif isinstance(tab, cdp_util.Tab):
            self.page = tab
        else:
            raise Exception("`tab` must be an int or a Tab type!")
        self.bring_active_window_to_front()

    def switch_to_newest_tab(self):
        self.switch_to_tab(-1)

    def close_active_tab(self):
        """Close the active tab.
        The active tab is the one currenly controlled by CDP.
        The active tab MIGHT NOT be the currently visible tab!
        (If a page opens a new tab, the new tab WON'T be active)
        To switch the active tab, call: sb.switch_to_tab(tab)"""
        return self.loop.run_until_complete(self.page.close())

    def get_active_tab(self):
        """Return the active tab.
        The active tab is the one currenly controlled by CDP.
        The active tab MIGHT NOT be the currently visible tab!
        (If a page opens a new tab, the new tab WON'T be active)
        To switch the active tab, call: sb.switch_to_tab(tab)"""
        return self.page

    def get_tabs(self):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return driver.tabs

    def get_window(self):
        return self.loop.run_until_complete(self.page.get_window())

    def get_text(self, selector):
        return self.find_element(selector).text_all

    def get_title(self):
        return self.loop.run_until_complete(
            self.page.evaluate("document.title")
        )

    def get_current_url(self):
        return self.loop.run_until_complete(
            self.page.evaluate("window.location.href")
        )

    def get_origin(self):
        return self.loop.run_until_complete(
            self.page.evaluate("window.location.origin")
        )

    def get_page_source(self):
        try:
            source = self.loop.run_until_complete(
                self.page.evaluate("document.documentElement.outerHTML")
            )
        except Exception:
            time.sleep(constants.UC.CDP_MODE_OPEN_WAIT)
            source = self.loop.run_until_complete(
                self.page.evaluate("document.documentElement.outerHTML")
            )
        return source

    def get_user_agent(self):
        return self.loop.run_until_complete(
            self.page.evaluate("navigator.userAgent")
        )

    def get_cookie_string(self):
        return self.loop.run_until_complete(
            self.page.evaluate("document.cookie")
        )

    def get_locale_code(self):
        return self.loop.run_until_complete(
            self.page.evaluate("navigator.language || navigator.languages[0]")
        )

    def get_local_storage_item(self, key):
        js_code = """localStorage.getItem('%s');""" % key
        with suppress(Exception):
            return self.loop.run_until_complete(self.page.evaluate(js_code))

    def get_session_storage_item(self, key):
        js_code = """sessionStorage.getItem('%s');""" % key
        with suppress(Exception):
            return self.loop.run_until_complete(self.page.evaluate(js_code))

    def get_screen_rect(self):
        coordinates = self.loop.run_until_complete(
            self.page.js_dumps("window.screen")
        )
        return coordinates

    def get_window_rect(self):
        coordinates = {}
        innerWidth = self.loop.run_until_complete(
            self.page.evaluate("window.innerWidth")
        )
        innerHeight = self.loop.run_until_complete(
            self.page.evaluate("window.innerHeight")
        )
        outerWidth = self.loop.run_until_complete(
            self.page.evaluate("window.outerWidth")
        )
        outerHeight = self.loop.run_until_complete(
            self.page.evaluate("window.outerHeight")
        )
        pageXOffset = self.loop.run_until_complete(
            self.page.evaluate("window.pageXOffset")
        )
        pageYOffset = self.loop.run_until_complete(
            self.page.evaluate("window.pageYOffset")
        )
        scrollX = self.loop.run_until_complete(
            self.page.evaluate("window.scrollX")
        )
        scrollY = self.loop.run_until_complete(
            self.page.evaluate("window.scrollY")
        )
        screenLeft = self.loop.run_until_complete(
            self.page.evaluate("window.screenLeft")
        )
        screenTop = self.loop.run_until_complete(
            self.page.evaluate("window.screenTop")
        )
        x = self.loop.run_until_complete(
            self.page.evaluate("window.screenX")
        )
        y = self.loop.run_until_complete(
            self.page.evaluate("window.screenY")
        )
        coordinates["innerWidth"] = innerWidth
        coordinates["innerHeight"] = innerHeight
        coordinates["outerWidth"] = outerWidth
        coordinates["outerHeight"] = outerHeight
        coordinates["width"] = outerWidth
        coordinates["height"] = outerHeight
        coordinates["pageXOffset"] = pageXOffset if pageXOffset else 0
        coordinates["pageYOffset"] = pageYOffset if pageYOffset else 0
        coordinates["scrollX"] = scrollX if scrollX else 0
        coordinates["scrollY"] = scrollY if scrollY else 0
        coordinates["screenLeft"] = screenLeft if screenLeft else 0
        coordinates["screenTop"] = screenTop if screenTop else 0
        coordinates["x"] = x if x else 0
        coordinates["y"] = y if y else 0
        return coordinates

    def get_window_size(self):
        coordinates = {}
        outerWidth = self.loop.run_until_complete(
            self.page.evaluate("window.outerWidth")
        )
        outerHeight = self.loop.run_until_complete(
            self.page.evaluate("window.outerHeight")
        )
        coordinates["width"] = outerWidth
        coordinates["height"] = outerHeight
        return coordinates

    def get_window_position(self):
        coordinates = {}
        x = self.loop.run_until_complete(
            self.page.evaluate("window.screenX")
        )
        y = self.loop.run_until_complete(
            self.page.evaluate("window.screenY")
        )
        coordinates["x"] = x if x else 0
        coordinates["y"] = y if y else 0
        return coordinates

    def get_element_rect(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.select(selector, timeout=timeout)
        self.__add_light_pause()
        coordinates = None
        if ":contains(" in selector:
            position = element.get_position()
            x = position.x
            y = position.y
            width = position.width
            height = position.height
            coordinates = {"x": x, "y": y, "width": width, "height": height}
        else:
            coordinates = self.loop.run_until_complete(
                self.page.js_dumps(
                    """document.querySelector('%s').getBoundingClientRect()"""
                    % js_utils.escape_quotes_if_needed(re.escape(selector))
                )
            )
        return coordinates

    def get_element_size(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = self.get_element_rect(selector, timeout=timeout)
        coordinates = {}
        coordinates["width"] = element_rect["width"]
        coordinates["height"] = element_rect["height"]
        return coordinates

    def get_element_position(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = self.get_element_rect(selector, timeout=timeout)
        coordinates = {}
        coordinates["x"] = element_rect["x"]
        coordinates["y"] = element_rect["y"]
        return coordinates

    def get_gui_element_rect(self, selector, timeout=None):
        """(Coordinates are relative to the screen. Not the window.)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = self.get_element_rect(selector, timeout=timeout)
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        window_rect = self.get_window_rect()
        w_bottom_y = window_rect["y"] + window_rect["height"]
        viewport_height = window_rect["innerHeight"]
        x = window_rect["x"] + element_rect["x"]
        y = w_bottom_y - viewport_height + element_rect["y"]
        y_scroll_offset = window_rect["pageYOffset"]
        y = y - y_scroll_offset
        x = x + window_rect["scrollX"]
        y = y + window_rect["scrollY"]
        return ({"height": e_height, "width": e_width, "x": x, "y": y})

    def get_gui_element_center(self, selector, timeout=None):
        """(Coordinates are relative to the screen. Not the window.)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = self.get_gui_element_rect(selector, timeout=timeout)
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        return ((e_x + e_width / 2.0) + 0.5, (e_y + e_height / 2.0) + 0.5)

    def get_document(self):
        return self.loop.run_until_complete(self.page.get_document())

    def get_flattened_document(self):
        return self.loop.run_until_complete(self.page.get_flattened_document())

    def get_element_attributes(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        return self.loop.run_until_complete(
            self.page.js_dumps(
                """document.querySelector('%s')"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

    def get_element_attribute(self, selector, attribute):
        """Find an element and return the value of an attribute.
        Raises an exception if there's no such element or attribute."""
        attributes = self.get_element_attributes(selector)
        with suppress(Exception):
            return attributes[attribute]
        locate = ' %s="' % attribute
        value = self.get_attribute(selector, attribute)
        if not value and locate not in attributes:
            raise KeyError(attribute)
        return value

    def get_attribute(self, selector, attribute):
        """Find an element and return the value of an attribute.
        If the element doesn't exist: Raises an exception.
        If the attribute doesn't exist: Returns None."""
        return self.find_element(selector).get_attribute(attribute)

    def get_element_html(self, selector):
        """Find an element and return the outerHTML."""
        selector = self.__convert_to_css_if_xpath(selector)
        self.find_element(selector)
        self.__add_light_pause()
        return self.loop.run_until_complete(
            self.page.evaluate(
                """document.querySelector('%s').outerHTML"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

    def set_locale(self, locale):
        """(Settings will take effect on the next page load)"""
        self.loop.run_until_complete(self.page.set_locale(locale))

    def set_local_storage_item(self, key, value):
        js_code = """localStorage.setItem('%s','%s');""" % (key, value)
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))

    def set_session_storage_item(self, key, value):
        js_code = """sessionStorage.setItem('%s','%s');""" % (key, value)
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))

    def set_attributes(self, selector, attribute, value):
        """This method uses JavaScript to set/update a common attribute.
        All matching selectors from querySelectorAll() are used.
        Example => (Make all links on a website redirect to Google):
        self.set_attributes("a", "href", "https://google.com")"""
        attribute = re.escape(attribute)
        attribute = js_utils.escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = js_utils.escape_quotes_if_needed(value)
        css_selector = self.__convert_to_css_if_xpath(selector)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        js_code = """var $elements = document.querySelectorAll('%s');
                  var index = 0, length = $elements.length;
                  for(; index < length; index++){
                  $elements[index].setAttribute('%s','%s');}""" % (
            css_selector,
            attribute,
            value,
        )
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))

    def __make_sure_pyautogui_lock_is_writable(self):
        with suppress(Exception):
            shared_utils.make_writable(constants.MultiBrowser.PYAUTOGUILOCK)

    def __verify_pyautogui_has_a_headed_browser(self):
        """PyAutoGUI requires a headed browser so that it can
        focus on the correct element when performing actions."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        if driver.config.headless:
            raise Exception(
                "PyAutoGUI can't be used in headless mode!"
            )

    def __install_pyautogui_if_missing(self):
        self.__verify_pyautogui_has_a_headed_browser()
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:  # Prevent issues with multiple processes
            with suppress(Exception):
                shared_utils.make_writable(constants.PipInstall.FINDLOCK)
            try:
                import pyautogui
                with suppress(Exception):
                    use_pyautogui_ver = constants.PyAutoGUI.VER
                    if pyautogui.__version__ != use_pyautogui_ver:
                        del pyautogui
                        shared_utils.pip_install(
                            "pyautogui", version=use_pyautogui_ver
                        )
                        import pyautogui
            except Exception:
                print("\nPyAutoGUI required! Installing now...")
                shared_utils.pip_install(
                    "pyautogui", version=constants.PyAutoGUI.VER
                )
                try:
                    import pyautogui
                except Exception:
                    if (
                        shared_utils.is_linux()
                        and (not sb_config.headed or sb_config.xvfb)
                        and not driver.config.headless
                        and (
                            not hasattr(sb_config, "_virtual_display")
                            or not sb_config._virtual_display
                        )
                    ):
                        from sbvirtualdisplay import Display
                        xvfb_width = 1366
                        xvfb_height = 768
                        if (
                            hasattr(sb_config, "_xvfb_width")
                            and sb_config._xvfb_width
                            and isinstance(sb_config._xvfb_width, int)
                            and hasattr(sb_config, "_xvfb_height")
                            and sb_config._xvfb_height
                            and isinstance(sb_config._xvfb_height, int)
                        ):
                            xvfb_width = sb_config._xvfb_width
                            xvfb_height = sb_config._xvfb_height
                            if xvfb_width < 1024:
                                xvfb_width = 1024
                            sb_config._xvfb_width = xvfb_width
                            if xvfb_height < 768:
                                xvfb_height = 768
                            sb_config._xvfb_height = xvfb_height
                        with suppress(Exception):
                            xvfb_display = Display(
                                visible=True,
                                size=(xvfb_width, xvfb_height),
                                backend="xvfb",
                                use_xauth=True,
                            )
                            if "--debug-display" in sys.argv:
                                print(
                                    "Starting VDisplay from sb_cdp: (%s, %s)"
                                    % (xvfb_width, xvfb_height)
                                )
                            xvfb_display.start()

    def __get_configured_pyautogui(self, pyautogui_copy):
        if (
            shared_utils.is_linux()
            and hasattr(pyautogui_copy, "_pyautogui_x11")
            and "DISPLAY" in os.environ.keys()
        ):
            if (
                hasattr(sb_config, "_pyautogui_x11_display")
                and sb_config._pyautogui_x11_display
                and hasattr(pyautogui_copy._pyautogui_x11, "_display")
                and (
                    sb_config._pyautogui_x11_display
                    == pyautogui_copy._pyautogui_x11._display
                )
            ):
                pass
            else:
                import Xlib.display
                pyautogui_copy._pyautogui_x11._display = (
                    Xlib.display.Display(os.environ['DISPLAY'])
                )
                sb_config._pyautogui_x11_display = (
                    pyautogui_copy._pyautogui_x11._display
                )
        return pyautogui_copy

    def gui_press_key(self, key):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            pyautogui.press(key)
            time.sleep(0.044)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def gui_press_keys(self, keys):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            for key in keys:
                pyautogui.press(key)
                time.sleep(0.044)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def gui_write(self, text):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            pyautogui.write(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.sleep(0.025))

    def __gui_click_x_y(self, x, y, timeframe=0.25, uc_lock=False):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x > screen_width or y > screen_height:
            raise Exception(
                "PyAutoGUI cannot click on point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x, y, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:  # Prevent issues with multiple processes
                self.__make_sure_pyautogui_lock_is_writable()
                pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
                if timeframe >= 0.25:
                    time.sleep(0.056)  # Wait if moving at human-speed
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
                pyautogui.click(x=x, y=y)
        else:
            # Called from a method where the gui_lock is already active
            pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
            if timeframe >= 0.25:
                time.sleep(0.056)  # Wait if moving at human-speed
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
            pyautogui.click(x=x, y=y)

    def gui_click_x_y(self, x, y, timeframe=0.25):
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:  # Prevent issues with multiple processes
            self.__make_sure_pyautogui_lock_is_writable()
            self.__install_pyautogui_if_missing()
            import pyautogui
            pyautogui = self.__get_configured_pyautogui(pyautogui)
            width_ratio = 1.0
            if shared_utils.is_windows():
                window_rect = self.get_window_rect()
                width = window_rect["width"]
                height = window_rect["height"]
                win_x = window_rect["x"]
                win_y = window_rect["y"]
                scr_width = pyautogui.size().width
                self.maximize()
                self.__add_light_pause()
                win_width = self.get_window_size()["width"]
                width_ratio = round(float(scr_width) / float(win_width), 2)
                width_ratio += 0.01
                if width_ratio < 0.45 or width_ratio > 2.55:
                    width_ratio = 1.01
                sb_config._saved_width_ratio = width_ratio
                self.minimize()
                self.__add_light_pause()
                self.set_window_rect(win_x, win_y, width, height)
                self.__add_light_pause()
                x = x * width_ratio
                y = y * width_ratio
            self.bring_active_window_to_front()
            self.__gui_click_x_y(x, y, timeframe=timeframe, uc_lock=False)

    def gui_click_element(self, selector, timeframe=0.25):
        self.__slow_mode_pause_if_set()
        x, y = self.get_gui_element_center(selector)
        self.__add_light_pause()
        self.gui_click_x_y(x, y, timeframe=timeframe)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def __gui_drag_drop(self, x1, y1, x2, y2, timeframe=0.25, uc_lock=False):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x1 < 0 or y1 < 0 or x1 > screen_width or y1 > screen_height:
            raise Exception(
                "PyAutoGUI cannot drag-drop from point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x1, y1, screen_width, screen_height)
            )
        if x2 < 0 or y2 < 0 or x2 > screen_width or y2 > screen_height:
            raise Exception(
                "PyAutoGUI cannot drag-drop to point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x2, y2, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:  # Prevent issues with multiple processes
                pyautogui.moveTo(x1, y1, 0.25, pyautogui.easeOutQuad)
                self.__add_light_pause()
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x1, y1))
                pyautogui.dragTo(x2, y2, button="left", duration=timeframe)
        else:
            # Called from a method where the gui_lock is already active
            pyautogui.moveTo(x1, y1, 0.25, pyautogui.easeOutQuad)
            self.__add_light_pause()
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.dragTo(%s, %s)" % (x2, y2))
            pyautogui.dragTo(x2, y2, button="left", duration=timeframe)

    def gui_drag_drop_points(self, x1, y1, x2, y2, timeframe=0.35):
        """Use PyAutoGUI to drag-and-drop from one point to another.
        Can simulate click-and-hold when using the same point twice."""
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:  # Prevent issues with multiple processes
            self.__install_pyautogui_if_missing()
            import pyautogui
            pyautogui = self.__get_configured_pyautogui(pyautogui)
            width_ratio = 1.0
            if shared_utils.is_windows():
                window_rect = self.get_window_rect()
                width = window_rect["width"]
                height = window_rect["height"]
                win_x = window_rect["x"]
                win_y = window_rect["y"]
                scr_width = pyautogui.size().width
                self.maximize()
                self.__add_light_pause()
                win_width = self.get_window_size()["width"]
                width_ratio = round(float(scr_width) / float(win_width), 2)
                width_ratio += 0.01
                if width_ratio < 0.45 or width_ratio > 2.55:
                    width_ratio = 1.01
                sb_config._saved_width_ratio = width_ratio
                self.minimize()
                self.__add_light_pause()
                self.set_window_rect(win_x, win_y, width, height)
                self.__add_light_pause()
                x1 = x1 * width_ratio
                y1 = y1 * width_ratio
                x2 = x2 * width_ratio
                y2 = y2 * width_ratio
            self.bring_active_window_to_front()
            self.__gui_drag_drop(
                x1, y1, x2, y2, timeframe=timeframe, uc_lock=False
            )
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def gui_drag_and_drop(self, drag_selector, drop_selector, timeframe=0.35):
        """Use PyAutoGUI to drag-and-drop from one selector to another.
        Can simulate click-and-hold when using the same selector twice."""
        self.__slow_mode_pause_if_set()
        self.bring_active_window_to_front()
        x1, y1 = self.get_gui_element_center(drag_selector)
        self.__add_light_pause()
        x2, y2 = self.get_gui_element_center(drop_selector)
        self.__add_light_pause()
        self.gui_drag_drop_points(x1, y1, x2, y2, timeframe=timeframe)

    def gui_click_and_hold(self, selector, timeframe=0.35):
        """Use PyAutoGUI to click-and-hold a selector."""
        self.__slow_mode_pause_if_set()
        self.bring_active_window_to_front()
        x, y = self.get_gui_element_center(selector)
        self.__add_light_pause()
        self.gui_drag_drop_points(x, y, x, y, timeframe=timeframe)

    def __gui_hover_x_y(self, x, y, timeframe=0.25, uc_lock=False):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x > screen_width or y > screen_height:
            raise Exception(
                "PyAutoGUI cannot hover on point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x, y, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:  # Prevent issues with multiple processes
                pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
                time.sleep(0.056)
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x, y))
        else:
            # Called from a method where the gui_lock is already active
            pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
            time.sleep(0.056)
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x, y))

    def gui_hover_x_y(self, x, y, timeframe=0.25):
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:  # Prevent issues with multiple processes
            self.__install_pyautogui_if_missing()
            import pyautogui
            pyautogui = self.__get_configured_pyautogui(pyautogui)
            width_ratio = 1.0
            if (
                shared_utils.is_windows()
                and (
                    not hasattr(sb_config, "_saved_width_ratio")
                    or not sb_config._saved_width_ratio
                )
            ):
                window_rect = self.get_window_rect()
                width = window_rect["width"]
                height = window_rect["height"]
                win_x = window_rect["x"]
                win_y = window_rect["y"]
                if (
                    hasattr(sb_config, "_saved_width_ratio")
                    and sb_config._saved_width_ratio
                ):
                    width_ratio = sb_config._saved_width_ratio
                else:
                    scr_width = pyautogui.size().width
                    self.maximize()
                    self.__add_light_pause()
                    win_width = self.get_window_size()["width"]
                    width_ratio = round(float(scr_width) / float(win_width), 2)
                    width_ratio += 0.01
                    if width_ratio < 0.45 or width_ratio > 2.55:
                        width_ratio = 1.01
                    sb_config._saved_width_ratio = width_ratio
                self.set_window_rect(win_x, win_y, width, height)
                self.__add_light_pause()
                self.bring_active_window_to_front()
            elif (
                shared_utils.is_windows()
                and hasattr(sb_config, "_saved_width_ratio")
                and sb_config._saved_width_ratio
            ):
                width_ratio = sb_config._saved_width_ratio
                self.bring_active_window_to_front()
            if shared_utils.is_windows():
                x = x * width_ratio
                y = y * width_ratio
                self.__gui_hover_x_y(x, y, timeframe=timeframe, uc_lock=False)
                return
            self.bring_active_window_to_front()
            self.__gui_hover_x_y(x, y, timeframe=timeframe, uc_lock=False)

    def gui_hover_element(self, selector, timeframe=0.25):
        self.__slow_mode_pause_if_set()
        element_rect = self.get_gui_element_rect(selector)
        width = element_rect["width"]
        height = element_rect["height"]
        if width > 0 and height > 0:
            x, y = self.get_gui_element_center(selector)
            self.bring_active_window_to_front()
            self.__gui_hover_x_y(x, y, timeframe=timeframe)
            self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def gui_hover_and_click(self, hover_selector, click_selector):
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            self.bring_active_window_to_front()
            self.gui_hover_element(hover_selector)
            time.sleep(0.15)
            self.gui_hover_element(click_selector)
            self.click(click_selector)

    def internalize_links(self):
        """All `target="_blank"` links become `target="_self"`.
        This prevents those links from opening in a new tab."""
        self.set_attributes('[target="_blank"]', "target", "_self")

    def is_checked(self, selector):
        """Return True if checkbox (or radio button) is checked."""
        selector = self.__convert_to_css_if_xpath(selector)
        self.find_element(selector, timeout=settings.SMALL_TIMEOUT)
        return bool(self.get_element_attribute(selector, "checked"))

    def is_selected(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        return self.is_checked(selector)

    def check_if_unchecked(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        if not self.is_checked(selector):
            self.click(selector)

    def select_if_unselected(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        self.check_if_unchecked(selector)

    def uncheck_if_checked(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        if self.is_checked(selector):
            self.click(selector)

    def unselect_if_selected(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        self.uncheck_if_checked(selector)

    def is_element_present(self, selector):
        try:
            self.select(selector, timeout=0.01)
            return True
        except Exception:
            return False

    def is_element_visible(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        element = None
        if ":contains(" not in selector:
            try:
                element = self.select(selector, timeout=0.01)
            except Exception:
                return False
            if not element:
                return False
            try:
                position = element.get_position()
                return (position.width != 0 or position.height != 0)
            except Exception:
                return False
        else:
            with suppress(Exception):
                tag_name = selector.split(":contains(")[0].split(" ")[-1]
                text = selector.split(":contains(")[1].split(")")[0][1:-1]
                self.loop.run_until_complete(
                    self.page.select(tag_name, timeout=0.1)
                )
                self.loop.run_until_complete(self.page.find(text, timeout=0.1))
                return True
            return False

    def is_text_visible(self, text, selector="body"):
        selector = self.__convert_to_css_if_xpath(selector)
        text = text.strip()
        element = None
        try:
            element = self.find_element(selector, timeout=0.1)
        except Exception:
            return False
        with suppress(Exception):
            if text in element.text_all:
                return True
        return False

    def is_exact_text_visible(self, text, selector="body"):
        selector = self.__convert_to_css_if_xpath(selector)
        text = text.strip()
        element = None
        try:
            element = self.find_element(selector, timeout=0.1)
        except Exception:
            return False
        with suppress(Exception):
            if text == element.text_all.strip():
                return True
        return False

    def wait_for_text(self, text, selector="body", timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        text = text.strip()
        element = None
        try:
            element = self.find_element(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(int(timeout * 10)):
            with suppress(Exception):
                element = self.find_element(selector, timeout=0.1)
            if text in element.text_all:
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        raise Exception(
            "Text {%s} not found in {%s}! Actual text: {%s}"
            % (text, selector, element.text_all)
        )

    def wait_for_text_not_visible(self, text, selector="body", timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        text = text.strip()
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not self.is_text_visible(text, selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Text {%s} in {%s} was still visible after %s second%s!"
            % (text, selector, timeout, plural)
        )

    def wait_for_element_visible(self, selector, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        try:
            self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} was not found!" % selector)
        for i in range(30):
            if self.is_element_visible(selector):
                return self.select(selector)
            time.sleep(0.1)
        raise Exception("Element {%s} was not visible!" % selector)

    def wait_for_element_not_visible(self, selector, timeout=None):
        """Wait for element to not be visible on page. (May still be in DOM)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not self.is_element_present(selector):
                return True
            elif not self.is_element_visible(selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Element {%s} was still visible after %s second%s!"
            % (selector, timeout, plural)
        )

    def wait_for_element_absent(self, selector, timeout=None):
        """Wait for element to not be present in the DOM."""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not self.is_element_present(selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Element {%s} was still present after %s second%s!"
            % (selector, timeout, plural)
        )

    def wait_for_any_of_elements_visible(self, *args, **kwargs):
        """Waits for at least one of the elements to be visible.
        Returns the first element that is found.
        The input is a list of elements. (Should be CSS selectors)
        Optional kwargs include: "timeout" (used by all selectors).
        Raises an exception if no elements are visible by the timeout.
        Examples:
            sb.cdp.wait_for_any_of_elements_visible("h1", "h2", "h3")
            OR
            sb.cdp.wait_for_any_of_elements_visible(["h1", "h2", "h3"]) """
        selectors = []
        timeout = None
        for kwarg in kwargs:
            if kwarg == "timeout":
                timeout = kwargs["timeout"]
            elif kwarg == "by":
                pass  # Autodetected
            elif kwarg == "selector" or kwarg == "selectors":
                selector = kwargs[kwarg]
                if isinstance(selector, str):
                    selectors.append(selector)
                elif isinstance(selector, list):
                    selectors_list = selector
                    for selector in selectors_list:
                        if isinstance(selector, str):
                            selectors.append(selector)
            else:
                raise Exception('Unknown kwarg: "%s"!' % kwarg)
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        for arg in args:
            if isinstance(arg, list):
                for selector in arg:
                    if isinstance(selector, str):
                        selectors.append(selector)
            elif isinstance(arg, str):
                selectors.append(arg)
        if not selectors:
            raise Exception("The selectors list was empty!")
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        any_present = False
        for i in range(int(timeout * 10)):
            for selector in selectors:
                if self.is_element_visible(selector):
                    return self.select(selector)
                if self.is_element_present(selector):
                    any_present = True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        if not any_present:
            # None of the elements exist in the HTML
            raise Exception(
                "None of the elements {%s} were present after %s second%s!" % (
                    str(selectors),
                    timeout,
                    plural,
                )
            )
        raise Exception(
            "None of the elements %s were visible after %s second%s!" % (
                str(selectors),
                timeout,
                plural,
            )
        )

    def wait_for_any_of_elements_present(self, *args, **kwargs):
        """Waits for at least one of the elements to be present.
        Visibility not required, but element must be in the DOM.
        Returns the first element that is found.
        The input is a list of elements. (Should be CSS selectors)
        Optional kwargs include: "timeout" (used by all selectors).
        Raises an exception if no elements are present by the timeout.
        Examples:
            self.wait_for_any_of_elements_present("style", "script")
            OR
            self.wait_for_any_of_elements_present(["style", "script"]) """
        selectors = []
        timeout = None
        for kwarg in kwargs:
            if kwarg == "timeout":
                timeout = kwargs["timeout"]
            elif kwarg == "by":
                pass  # Autodetected
            elif kwarg == "selector" or kwarg == "selectors":
                selector = kwargs[kwarg]
                if isinstance(selector, str):
                    selectors.append(selector)
                elif isinstance(selector, list):
                    selectors_list = selector
                    for selector in selectors_list:
                        if isinstance(selector, str):
                            selectors.append(selector)
            else:
                raise Exception('Unknown kwarg: "%s"!' % kwarg)
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        for arg in args:
            if isinstance(arg, list):
                for selector in arg:
                    if isinstance(selector, str):
                        selectors.append(selector)
            elif isinstance(arg, str):
                selectors.append(arg)
        if not selectors:
            raise Exception("The selectors list was empty!")
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            for selector in selectors:
                if self.is_element_present(selector):
                    return self.select(selector)
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        # None of the elements exist in the HTML
        raise Exception(
            "None of the elements %s were present after %s second%s!" % (
                str(selectors),
                timeout,
                plural,
            )
        )

    def assert_any_of_elements_visible(self, *args, **kwargs):
        """Like wait_for_any_of_elements_visible(), but returns nothing."""
        self.wait_for_any_of_elements_visible(*args, **kwargs)
        return True

    def assert_any_of_elements_present(self, *args, **kwargs):
        """Like wait_for_any_of_elements_present(), but returns nothing."""
        self.wait_for_any_of_elements_present(*args, **kwargs)
        return True

    def assert_element(self, selector, timeout=None):
        """Same as assert_element_visible()"""
        self.assert_element_visible(selector, timeout=timeout)
        return True

    def assert_element_visible(self, selector, timeout=None):
        """Same as assert_element()"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        try:
            self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} was not found!" % selector)
        for i in range(30):
            if self.is_element_visible(selector):
                return True
            time.sleep(0.1)
        raise Exception("Element {%s} was not visible!" % selector)

    def assert_element_present(self, selector, timeout=None):
        """Assert element is present in the DOM. (Visibility NOT required)"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        try:
            self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} was not found!" % selector)
        return True

    def assert_element_absent(self, selector, timeout=None):
        """Assert element is not present in the DOM."""
        self.wait_for_element_absent(selector, timeout=timeout)
        return True

    def assert_element_not_visible(self, selector, timeout=None):
        """Assert element is not visible on page. (May still be in DOM)"""
        self.wait_for_element_not_visible(selector, timeout=timeout)
        return True

    def assert_element_attribute(self, selector, attribute, value=None):
        attributes = self.get_element_attributes(selector)
        if attribute not in attributes:
            raise Exception(
                "Attribute {%s} was not found in element {%s}!"
                % (attribute, selector)
            )
        if value and attributes[attribute] != value:
            raise Exception(
                "Expected value {%s} of attribute {%s} "
                "was not found in element {%s}! "
                "(Actual value was {%s})"
                % (value, attribute, selector, attributes[attribute])
            )

    def assert_title(self, title):
        expected = title.strip()
        actual = self.get_title().strip()
        error = (
            "Expected page title [%s] does not match the actual title [%s]!"
        )
        try:
            if expected != actual:
                raise Exception(error % (expected, actual))
        except Exception:
            time.sleep(2)
            actual = self.get_title().strip()
            if expected != actual:
                raise Exception(error % (expected, actual))

    def assert_title_contains(self, substring):
        expected = substring.strip()
        actual = self.get_title().strip()
        error = (
            "Expected title substring [%s] does not appear "
            "in the actual page title [%s]!"
        )
        try:
            if expected not in actual:
                raise Exception(error % (expected, actual))
        except Exception:
            time.sleep(2)
            actual = self.get_title().strip()
            if expected not in actual:
                raise Exception(error % (expected, actual))

    def assert_url(self, url):
        expected = url.strip()
        actual = self.get_current_url().strip()
        error = "Expected URL [%s] does not match the actual URL [%s]!"
        try:
            if expected != actual:
                raise Exception(error % (expected, actual))
        except Exception:
            time.sleep(2)
            actual = self.get_current_url().strip()
            if expected != actual:
                raise Exception(error % (expected, actual))

    def assert_url_contains(self, substring):
        expected = substring.strip()
        actual = self.get_current_url().strip()
        error = (
            "Expected URL substring [%s] does not appear "
            "in the full URL [%s]!"
        )
        try:
            if expected not in actual:
                raise Exception(error % (expected, actual))
        except Exception:
            time.sleep(2)
            actual = self.get_current_url().strip()
            if expected not in actual:
                raise Exception(error % (expected, actual))

    def assert_text(self, text, selector="body", timeout=None):
        """Same as wait_for_text()"""
        self.wait_for_text(text, selector=selector, timeout=timeout)
        return True

    def assert_exact_text(self, text, selector="body", timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        text = text.strip()
        element = None
        try:
            element = self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(int(timeout * 10)):
            with suppress(Exception):
                element = self.select(selector, timeout=0.1)
            if (
                self.is_element_visible(selector)
                and text.strip() == element.text_all.strip()
            ):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        raise Exception(
            "Expected Text {%s}, is not equal to {%s} in {%s}!"
            % (text, element.text_all, selector)
        )

    def assert_text_not_visible(self, text, selector="body", timeout=None):
        """Raises an exception if the text is still visible after timeout."""
        self.wait_for_text_not_visible(
            text, selector=selector, timeout=timeout
        )
        return True

    def assert_true(self, expression):
        if not expression:
            raise AssertionError("%s is not true" % expression)

    def assert_false(self, expression):
        if expression:
            raise AssertionError("%s is not false" % expression)

    def assert_equal(self, first, second):
        if first != second:
            raise AssertionError("%s is not equal to %s" % (first, second))

    def assert_not_equal(self, first, second):
        if first == second:
            raise AssertionError("%s is equal to %s" % (first, second))

    def assert_in(self, first, second):
        if first not in second:
            raise AssertionError("%s is not in %s" % (first, second))

    def assert_not_in(self, first, second):
        if first in second:
            raise AssertionError("%s is in %s" % (first, second))

    def scroll_into_view(self, selector):
        self.find_element(selector).scroll_into_view()
        self.loop.run_until_complete(self.page.wait())

    def scroll_to_y(self, y):
        y = int(y)
        js_code = "window.scrollTo(0, %s);" % y
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))
            self.loop.run_until_complete(self.page.wait())

    def scroll_to_top(self):
        js_code = "window.scrollTo(0, 0);"
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))
            self.loop.run_until_complete(self.page.wait())

    def scroll_to_bottom(self):
        js_code = "window.scrollTo(0, 10000);"
        with suppress(Exception):
            self.loop.run_until_complete(self.page.evaluate(js_code))
            self.loop.run_until_complete(self.page.wait())

    def scroll_up(self, amount=25):
        self.loop.run_until_complete(self.page.scroll_up(amount))
        self.loop.run_until_complete(self.page.wait())

    def scroll_down(self, amount=25):
        self.loop.run_until_complete(self.page.scroll_down(amount))
        self.loop.run_until_complete(self.page.wait())

    def save_screenshot(self, name, folder=None, selector=None):
        filename = name
        if folder:
            filename = os.path.join(folder, name)
        if not selector:
            self.loop.run_until_complete(
                self.page.save_screenshot(filename)
            )
        else:
            self.select(selector).save_screenshot(filename)

    def print_to_pdf(self, name, folder=None):
        filename = name
        if folder:
            filename = os.path.join(folder, name)
        self.loop.run_until_complete(self.page.print_to_pdf(filename))


class Chrome(CDPMethods):
    def __init__(self, url=None, **kwargs):
        if not url:
            url = "about:blank"
        loop = asyncio.new_event_loop()
        driver = cdp_util.start_sync(**kwargs)
        page = loop.run_until_complete(driver.get(url))
        super().__init__(loop, page, driver)
