"""Add CDP methods to extend the driver"""
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


class CDPMethods():
    def __init__(self, loop, page, driver):
        self.loop = loop
        self.page = page
        self.driver = driver

    def __slow_mode_pause_if_set(self):
        if hasattr(sb_config, "slow_mode") and sb_config.slow_mode:
            time.sleep(0.16)

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
        element.highlight_overlay = lambda: self.__highlight_overlay(element)
        element.mouse_click = lambda: self.__mouse_click(element)
        element.mouse_drag = (
            lambda destination: self.__mouse_drag(element, destination)
        )
        element.mouse_move = lambda: self.__mouse_move(element)
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
        return element

    def get(self, url):
        url = shared_utils.fix_url_as_needed(url)
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        self.page = self.loop.run_until_complete(driver.get(url))
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

    def open(self, url):
        self.get(url)

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

    def find_element(
        self, selector, best_match=False, timeout=settings.SMALL_TIMEOUT
    ):
        """Similar to select(), but also finds elements by text content.
        When using text-based searches, if best_match=False, then will
        find the first element with the text. If best_match=True, then
        if multiple elements have that text, then will use the element
        with the closest text-length to the text being searched for."""
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        early_failure = False
        if (":contains(" in selector):
            tag_name = selector.split(":contains(")[0].split(" ")[-1]
            text = selector.split(":contains(")[1].split(")")[0][1:-1]
            with suppress(Exception):
                self.loop.run_until_complete(
                    self.page.select(tag_name, timeout=timeout)
                )
                self.loop.run_until_complete(
                    self.page.find(text, timeout=timeout)
                )
            elements = []
            with suppress(Exception):
                elements = self.find_elements_by_text(text, tag_name=tag_name)
            if elements:
                return self.__add_sync_methods(elements[0])
            else:
                early_failure = True
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

    def find_all(self, selector, timeout=settings.SMALL_TIMEOUT):
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        elements = self.loop.run_until_complete(
            self.page.find_all(selector, timeout=timeout)
        )
        updated_elements = []
        for element in elements:
            element = self.__add_sync_methods(element)
            updated_elements.append(element)
        self.__slow_mode_pause_if_set()
        return updated_elements

    def find_elements_by_text(self, text, tag_name=None):
        """Returns a list of elements by matching text.
        Optionally, provide a tag_name to narrow down the search
        to only elements with the given tag. (Eg: a, div, script, span)"""
        self.__add_light_pause()
        elements = self.loop.run_until_complete(
            self.page.find_elements_by_text(text=text)
        )
        updated_elements = []
        for element in elements:
            if (
                not tag_name
                or tag_name.lower().strip() in element.tag_name.lower().strip()
            ):
                element = self.__add_sync_methods(element)
                updated_elements.append(element)
        self.__slow_mode_pause_if_set()
        return updated_elements

    def select(self, selector, timeout=settings.SMALL_TIMEOUT):
        """Similar to find_element(), but without text-based search."""
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        if (":contains(" in selector):
            tag_name = selector.split(":contains(")[0].split(" ")[-1]
            text = selector.split(":contains(")[1].split(")")[0][1:-1]
            with suppress(Exception):
                self.loop.run_until_complete(
                    self.page.select(tag_name, timeout=5)
                )
                self.loop.run_until_complete(self.page.find(text, timeout=5))
            element = self.find_elements_by_text(text, tag_name=tag_name)[0]
            return self.__add_sync_methods(element)
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

    def select_all(self, selector, timeout=settings.SMALL_TIMEOUT):
        self.__add_light_pause()
        selector = self.__convert_to_css_if_xpath(selector)
        elements = self.loop.run_until_complete(
            self.page.select_all(selector, timeout=timeout)
        )
        updated_elements = []
        for element in elements:
            element = self.__add_sync_methods(element)
            updated_elements.append(element)
        self.__slow_mode_pause_if_set()
        return updated_elements

    def find_elements(self, selector, timeout=settings.SMALL_TIMEOUT):
        return self.select_all(selector, timeout=timeout)

    def find_visible_elements(self, selector, timeout=settings.SMALL_TIMEOUT):
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
        element.click()

    def click_link(self, link_text):
        self.find_elements_by_text(link_text, "a")[0].click()

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
        return (
            self.loop.run_until_complete(
                element.flash_async(*args, **kwargs)
            )
        )

    def __focus(self, element):
        return (
            self.loop.run_until_complete(element.focus_async())
        )

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
        return (
            self.loop.run_until_complete(element.scroll_into_view_async())
        )

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

    def tile_windows(self, windows=None, max_columns=0):
        """Tile windows and return the grid of tiled windows."""
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.tile_windows(windows, max_columns)
        )

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

    def clear_cookies(self, *args, **kwargs):
        driver = self.driver
        if hasattr(driver, "cdp_base"):
            driver = driver.cdp_base
        return self.loop.run_until_complete(
            driver.cookies.clear(*args, **kwargs)
        )

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
        return self.loop.run_until_complete(
            self.page.evaluate(js_code)
        )

    def click(self, selector, timeout=settings.SMALL_TIMEOUT):
        self.__slow_mode_pause_if_set()
        element = self.find_element(selector, timeout=timeout)
        self.__add_light_pause()
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
            self.find_element(selector).click()
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
                    element.click()
                    click_count += 1
                    time.sleep(0.0375)
                    self.__slow_mode_pause_if_set()
                    self.loop.run_until_complete(self.page.wait())
            except Exception:
                break

    def mouse_click(self, selector, timeout=settings.SMALL_TIMEOUT):
        """(Attempt simulating a mouse click)"""
        self.__slow_mode_pause_if_set()
        element = self.find_element(selector, timeout=timeout)
        self.__add_light_pause()
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
        element.flash(duration=duration, color=color)
        if pause and isinstance(pause, (int, float)):
            time.sleep(pause)

    def highlight(self, selector):
        """Highlight an element with multi-colors."""
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.find_element(selector)
        element.flash(0.46, "44CC88")
        time.sleep(0.15)
        element.flash(0.42, "8844CC")
        time.sleep(0.15)
        element.flash(0.38, "CC8844")
        time.sleep(0.15)
        element.flash(0.30, "44CC88")
        time.sleep(0.30)

    def focus(self, selector):
        self.find_element(selector).focus()

    def highlight_overlay(self, selector):
        self.find_element(selector).highlight_overlay()

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

    def send_keys(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        self.__add_light_pause()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def press_keys(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        """Similar to send_keys(), but presses keys at human speed."""
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        self.__add_light_pause()
        submit = False
        if text.endswith("\n") or text.endswith("\r"):
            submit = True
            text = text[:-1]
        for key in text:
            element.send_keys(key)
            time.sleep(0.0375)
        if submit:
            element.send_keys("\r\n")
            time.sleep(0.0375)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def type(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        """Similar to send_keys(), but clears the text field first."""
        self.__slow_mode_pause_if_set()
        element = self.select(selector, timeout=timeout)
        self.__add_light_pause()
        with suppress(Exception):
            element.clear_input()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def set_value(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        """Similar to send_keys(), but clears the text field first."""
        self.__slow_mode_pause_if_set()
        selector = self.__convert_to_css_if_xpath(selector)
        self.select(selector, timeout=timeout)
        self.__add_light_pause()
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
        self.loop.run_until_complete(self.page.wait())

    def evaluate(self, expression):
        """Run a JavaScript expression and return the result."""
        return self.loop.run_until_complete(
            self.page.evaluate(expression)
        )

    def js_dumps(self, obj_name):
        """Similar to evaluate(), but for dictionary results."""
        return self.loop.run_until_complete(
            self.page.js_dumps(obj_name)
        )

    def maximize(self):
        if self.get_window()[1].window_state.value == "maximized":
            return
        elif self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(self.page.maximize())
            time.sleep(0.0375)
        return self.loop.run_until_complete(self.page.maximize())

    def minimize(self):
        if self.get_window()[1].window_state.value != "minimized":
            return self.loop.run_until_complete(self.page.minimize())

    def medimize(self):
        if self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(self.page.medimize())
            time.sleep(0.0375)
        return self.loop.run_until_complete(self.page.medimize())

    def set_window_rect(self, x, y, width, height):
        if self.get_window()[1].window_state.value == "minimized":
            self.loop.run_until_complete(
                self.page.set_window_size(
                    left=x, top=y, width=width, height=height)
            )
            time.sleep(0.0375)
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

    def get_window(self):
        return self.loop.run_until_complete(
            self.page.get_window()
        )

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

    def get_element_rect(self, selector, timeout=settings.SMALL_TIMEOUT):
        selector = self.__convert_to_css_if_xpath(selector)
        self.select(selector, timeout=timeout)
        self.__add_light_pause()
        coordinates = self.loop.run_until_complete(
            self.page.js_dumps(
                """document.querySelector"""
                """('%s').getBoundingClientRect()"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )
        return coordinates

    def get_element_size(self, selector):
        element_rect = self.get_element_rect(selector)
        coordinates = {}
        coordinates["width"] = element_rect["width"]
        coordinates["height"] = element_rect["height"]
        return coordinates

    def get_element_position(self, selector):
        element_rect = self.get_element_rect(selector)
        coordinates = {}
        coordinates["x"] = element_rect["x"]
        coordinates["y"] = element_rect["y"]
        return coordinates

    def get_gui_element_rect(self, selector):
        """(Coordinates are relative to the screen. Not the window.)"""
        element_rect = self.get_element_rect(selector)
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

    def get_gui_element_center(self, selector):
        """(Coordinates are relative to the screen. Not the window.)"""
        element_rect = self.get_gui_element_rect(selector)
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        return ((e_x + e_width / 2.0) + 0.5, (e_y + e_height / 2.0) + 0.5)

    def get_document(self):
        return self.loop.run_until_complete(
            self.page.get_document()
        )

    def get_flattened_document(self):
        return self.loop.run_until_complete(
            self.page.get_flattened_document()
        )

    def get_element_attributes(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        return self.loop.run_until_complete(
            self.page.js_dumps(
                """document.querySelector('%s')"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

    def get_element_attribute(self, selector, attribute):
        attributes = self.get_element_attributes(selector)
        return attributes[attribute]

    def get_element_html(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        return self.loop.run_until_complete(
            self.page.evaluate(
                """document.querySelector('%s').outerHTML"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

    def set_locale(self, locale):
        """(Settings will take effect on the next page load)"""
        self.loop.run_until_complete(self.page.set_locale(locale))

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
            pyautogui.press(key)
            time.sleep(0.0375)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def gui_press_keys(self, keys):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            for key in keys:
                pyautogui.press(key)
                time.sleep(0.0375)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

    def gui_write(self, text):
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            pyautogui.write(text)
        self.__slow_mode_pause_if_set()
        self.loop.run_until_complete(self.page.wait())

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
        self.__slow_mode_pause_if_set()
        self.bring_active_window_to_front()
        x1, y1 = self.get_gui_element_center(drag_selector)
        self.__add_light_pause()
        x2, y2 = self.get_gui_element_center(drop_selector)
        self.__add_light_pause()
        self.gui_drag_drop_points(x1, y1, x2, y2, timeframe=timeframe)

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
        return self.get_element_attribute(selector, "checked")

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

    def assert_element(self, selector, timeout=settings.SMALL_TIMEOUT):
        try:
            self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(30):
            if self.is_element_visible(selector):
                return True
            time.sleep(0.1)
        raise Exception("Element {%s} not visible!" % selector)

    def assert_element_present(self, selector, timeout=settings.SMALL_TIMEOUT):
        try:
            self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        return True

    def assert_element_absent(self, selector, timeout=settings.SMALL_TIMEOUT):
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

    def assert_element_not_visible(
        self, selector, timeout=settings.SMALL_TIMEOUT
    ):
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
            expected = title.strip()
            actual = self.get_title().strip()
            if expected != actual:
                raise Exception(error % (expected, actual))

    def assert_text(
        self, text, selector="html", timeout=settings.SMALL_TIMEOUT
    ):
        text = text.strip()
        element = None
        try:
            element = self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(30):
            if self.is_element_visible(selector) and text in element.text_all:
                return True
            time.sleep(0.1)
        raise Exception(
            "Text {%s} not found in {%s}! Actual text: {%s}"
            % (text, selector, element.text_all)
        )

    def assert_exact_text(
        self, text, selector="html", timeout=settings.SMALL_TIMEOUT
    ):
        text = text.strip()
        element = None
        try:
            element = self.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(30):
            if (
                self.is_element_visible(selector)
                and text.strip() == element.text_all.strip()
            ):
                return True
            time.sleep(0.1)
        raise Exception(
            "Expected Text {%s}, is not equal to {%s} in {%s}!"
            % (text, element.text_all, selector)
        )

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
