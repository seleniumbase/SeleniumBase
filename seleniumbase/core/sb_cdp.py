"""Add CDP methods to extend the driver"""
import math
import os
import re
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
        element.flash = lambda: self.__flash(element)
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
        self.page = self.loop.run_until_complete(self.driver.cdp_base.get(url))
        url_protocol = url.split(":")[0]
        safe_url = True
        if url_protocol not in ["about", "data", "chrome"]:
            safe_url = False
        if not safe_url:
            time.sleep(constants.UC.CDP_MODE_OPEN_WAIT)

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
        if (":contains(" in selector):
            tag_name = selector.split(":contains(")[0].split(" ")[-1]
            text = selector.split(":contains(")[1].split(")")[0][1:-1]
            with suppress(Exception):
                self.loop.run_until_complete(
                    self.page.select(tag_name, timeout=3)
                )
                self.loop.run_until_complete(self.page.find(text, timeout=3))
            element = self.find_elements_by_text(text, tag_name=tag_name)[0]
            return self.__add_sync_methods(element)
        failure = False
        try:
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
            if not tag_name or tag_name.lower() == element.tag_name.lower():
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

    def click_link(self, link_text):
        self.find_elements_by_text(link_text, "a")[0].click()

    def __clear_input(self, element):
        return (
            self.loop.run_until_complete(element.clear_input_async())
        )

    def __click(self, element):
        return (
            self.loop.run_until_complete(element.click_async())
        )

    def __flash(self, element):
        return (
            self.loop.run_until_complete(element.flash_async())
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
        return (
            self.loop.run_until_complete(element.mouse_click_async())
        )

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
        element = self.loop.run_until_complete(
            element.query_selector_async(selector)
        )
        element = self.__add_sync_methods(element)
        return element

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
        return self.loop.run_until_complete(
            self.driver.cdp_base.tile_windows(windows, max_columns)
        )

    def get_all_cookies(self, *args, **kwargs):
        return self.loop.run_until_complete(
            self.driver.cdp_base.cookies.get_all(*args, **kwargs)
        )

    def set_all_cookies(self, *args, **kwargs):
        return self.loop.run_until_complete(
            self.driver.cdp_base.cookies.set_all(*args, **kwargs)
        )

    def save_cookies(self, *args, **kwargs):
        return self.loop.run_until_complete(
            self.driver.cdp_base.cookies.save(*args, **kwargs)
        )

    def load_cookies(self, *args, **kwargs):
        return self.loop.run_until_complete(
            self.driver.cdp_base.cookies.load(*args, **kwargs)
        )

    def clear_cookies(self, *args, **kwargs):
        return self.loop.run_until_complete(
            self.driver.cdp_base.cookies.clear(*args, **kwargs)
        )

    def sleep(self, seconds):
        time.sleep(seconds)

    def bring_active_window_to_front(self):
        self.loop.run_until_complete(self.page.bring_to_front())

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

    def click_active_element(self):
        self.loop.run_until_complete(
            self.page.evaluate("document.activeElement.click()")
        )
        self.__slow_mode_pause_if_set()

    def click_if_visible(self, selector):
        if self.is_element_visible(selector):
            self.find_element(selector).click()
            self.__slow_mode_pause_if_set()

    def mouse_click(self, selector, timeout=settings.SMALL_TIMEOUT):
        """(Attempt simulating a mouse click)"""
        self.__slow_mode_pause_if_set()
        element = self.find_element(selector, timeout=timeout)
        self.__add_light_pause()
        element.mouse_click()
        self.__slow_mode_pause_if_set()

    def nested_click(self, parent_selector, selector):
        """
        Find parent element and click on child element inside it.
        (This can be used to click on elements inside an iframe.)
        """
        element = self.find_element(parent_selector)
        element.query_selector(selector).mouse_click()
        self.__slow_mode_pause_if_set()

    def get_nested_element(self, parent_selector, selector):
        """(Can be used to find an element inside an iframe)"""
        element = self.find_element(parent_selector)
        return element.query_selector(selector)

    def flash(self, selector):
        """Paint a quickly-vanishing dot over an element."""
        self.find_element(selector).flash()

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

    def scroll_into_view(self, selector):
        self.find_element(selector).scroll_into_view()

    def send_keys(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        element = self.select(selector)
        self.__slow_mode_pause_if_set()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()

    def press_keys(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        """Similar to send_keys(), but presses keys at human speed."""
        element = self.select(selector)
        self.__slow_mode_pause_if_set()
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

    def type(self, selector, text, timeout=settings.SMALL_TIMEOUT):
        """Similar to send_keys(), but clears the text field first."""
        element = self.select(selector)
        self.__slow_mode_pause_if_set()
        with suppress(Exception):
            element.clear_input()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        element.send_keys(text)
        self.__slow_mode_pause_if_set()

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
        return self.loop.run_until_complete(
            self.page.maximize()
        )

    def minimize(self):
        return self.loop.run_until_complete(
            self.page.minimize()
        )

    def medimize(self):
        return self.loop.run_until_complete(
            self.page.medimize()
        )

    def set_window_rect(self, x, y, width, height):
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

    def get_element_rect(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
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
        x = math.ceil(window_rect["x"] + element_rect["x"])
        y = math.ceil(w_bottom_y - viewport_height + element_rect["y"])
        y_scroll_offset = window_rect["pageYOffset"]
        y = int(y - y_scroll_offset)
        return ({"height": e_height, "width": e_width, "x": x, "y": y})

    def get_gui_element_center(self, selector):
        """(Coordinates are relative to the screen. Not the window.)"""
        element_rect = self.get_gui_element_rect(selector)
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        return ((e_x + e_width / 2), (e_y + e_height / 2))

    def get_document(self):
        return self.loop.run_until_complete(
            self.page.get_document()
        )

    def get_flattened_document(self):
        return self.loop.run_until_complete(
            self.page.get_flattened_document()
        )

    def get_element_attributes(self, selector):
        return self.loop.run_until_complete(
            self.page.js_dumps(
                """document.querySelector('%s')"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

    def get_element_html(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        return self.loop.run_until_complete(
            self.page.evaluate(
                """document.querySelector('%s').outerHTML"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )

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

    def internalize_links(self):
        """All `target="_blank"` links become `target="_self"`.
        This prevents those links from opening in a new tab."""
        self.set_attributes('[target="_blank"]', "target", "_self")

    def is_element_present(self, selector):
        try:
            self.select(selector, timeout=0.01)
            return True
        except Exception:
            return False
        selector = self.__convert_to_css_if_xpath(selector)
        element = self.loop.run_until_complete(
            self.page.js_dumps(
                """document.querySelector('%s')"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        )
        return element is not None

    def is_element_visible(self, selector):
        selector = self.__convert_to_css_if_xpath(selector)
        element = None
        if ":contains(" not in selector:
            try:
                element = self.loop.run_until_complete(
                    self.page.js_dumps(
                        """window.getComputedStyle(document.querySelector"""
                        """('%s'))"""
                        % js_utils.escape_quotes_if_needed(re.escape(selector))
                    )
                )
            except Exception:
                return False
            if not element:
                return False
            return element.get("display") != "none"
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

    def assert_text(
        self, text, selector="html", timeout=settings.SMALL_TIMEOUT
    ):
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
