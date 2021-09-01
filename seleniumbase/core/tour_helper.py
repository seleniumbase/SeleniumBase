"""
This module contains methods for running website tours.
These helper methods SHOULD NOT be called directly from tests.
"""
import os
import re
import time
from selenium.webdriver.common.by import By
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.core import style_sheet
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions

EXPORTED_TOURS_FOLDER = constants.Tours.EXPORTED_TOURS_FOLDER


def activate_bootstrap(driver):
    """Allows you to use Bootstrap Tours with SeleniumBase
    http://bootstraptour.com/
    """
    bootstrap_tour_css = constants.BootstrapTour.MIN_CSS
    bootstrap_tour_js = constants.BootstrapTour.MIN_JS

    verify_script = """// Verify Bootstrap Tour activated
                     var tour2 = new Tour({
                     });"""

    backdrop_style = style_sheet.bt_backdrop_style
    js_utils.add_css_style(driver, backdrop_style)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    for x in range(4):
        js_utils.activate_jquery(driver)
        js_utils.add_css_link(driver, bootstrap_tour_css)
        js_utils.add_js_link(driver, bootstrap_tour_js)
        time.sleep(0.1)
        for x in range(int(settings.MINI_TIMEOUT * 2.0)):
            # Bootstrap needs a small amount of time to load & activate.
            try:
                driver.execute_script(verify_script)
                time.sleep(0.05)
                return
            except Exception:
                time.sleep(0.15)
    js_utils.raise_unable_to_load_jquery_exception(driver)


def is_bootstrap_activated(driver):
    verify_script = """// Verify Bootstrap Tour activated
                     var tour2 = new Tour({
                     });"""
    try:
        driver.execute_script(verify_script)
        return True
    except Exception:
        return False


def activate_driverjs(driver):
    """Allows you to use DriverJS Tours with SeleniumBase
    https://kamranahmed.info/driver.js/
    """
    backdrop_style = style_sheet.dt_backdrop_style
    driverjs_css = constants.DriverJS.MIN_CSS
    driverjs_js = constants.DriverJS.MIN_JS

    verify_script = """// Verify DriverJS activated
                     var driverjs2 = Driver.name;
                     """

    activate_bootstrap(driver)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    js_utils.add_css_style(driver, backdrop_style)
    for x in range(4):
        js_utils.activate_jquery(driver)
        js_utils.add_css_link(driver, driverjs_css)
        js_utils.add_js_link(driver, driverjs_js)
        time.sleep(0.1)
        for x in range(int(settings.MINI_TIMEOUT * 2.0)):
            # DriverJS needs a small amount of time to load & activate.
            try:
                driver.execute_script(verify_script)
                js_utils.wait_for_ready_state_complete(driver)
                js_utils.wait_for_angularjs(driver)
                time.sleep(0.05)
                return
            except Exception:
                time.sleep(0.15)
    js_utils.raise_unable_to_load_jquery_exception(driver)


def is_driverjs_activated(driver):
    verify_script = """// Verify DriverJS activated
                     var driverjs2 = Driver.name;
                     """
    try:
        driver.execute_script(verify_script)
        return True
    except Exception:
        return False


def activate_hopscotch(driver):
    """Allows you to use Hopscotch Tours with SeleniumBase
    http://linkedin.github.io/hopscotch/
    """
    hopscotch_css = constants.Hopscotch.MIN_CSS
    hopscotch_js = constants.Hopscotch.MIN_JS
    backdrop_style = style_sheet.hops_backdrop_style

    verify_script = """// Verify Hopscotch activated
                     var hops = hopscotch.isActive;
                     """

    activate_bootstrap(driver)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    js_utils.add_css_style(driver, backdrop_style)
    for x in range(4):
        js_utils.activate_jquery(driver)
        js_utils.add_css_link(driver, hopscotch_css)
        js_utils.add_js_link(driver, hopscotch_js)
        time.sleep(0.1)
        for x in range(int(settings.MINI_TIMEOUT * 2.0)):
            # Hopscotch needs a small amount of time to load & activate.
            try:
                driver.execute_script(verify_script)
                js_utils.wait_for_ready_state_complete(driver)
                js_utils.wait_for_angularjs(driver)
                time.sleep(0.05)
                return
            except Exception:
                time.sleep(0.15)
    js_utils.raise_unable_to_load_jquery_exception(driver)


def is_hopscotch_activated(driver):
    verify_script = """// Verify Hopscotch activated
                     var hops = hopscotch.isActive;
                     """
    try:
        driver.execute_script(verify_script)
        return True
    except Exception:
        return False


def activate_introjs(driver):
    """Allows you to use IntroJS Tours with SeleniumBase
    https://introjs.com/
    """
    intro_css = constants.IntroJS.MIN_CSS
    intro_js = constants.IntroJS.MIN_JS

    theme_color = sb_config.introjs_theme_color
    hover_color = sb_config.introjs_hover_color
    backdrop_style = style_sheet.introjs_style % (
        theme_color,
        hover_color,
        hover_color,
        hover_color,
        theme_color,
    )

    verify_script = """// Verify IntroJS activated
                     var intro2 = introJs();
                     """

    activate_bootstrap(driver)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    js_utils.add_css_style(driver, backdrop_style)
    for x in range(4):
        js_utils.activate_jquery(driver)
        js_utils.add_css_link(driver, intro_css)
        js_utils.add_js_link(driver, intro_js)
        time.sleep(0.1)
        for x in range(int(settings.MINI_TIMEOUT * 2.0)):
            # IntroJS needs a small amount of time to load & activate.
            try:
                driver.execute_script(verify_script)
                js_utils.wait_for_ready_state_complete(driver)
                js_utils.wait_for_angularjs(driver)
                time.sleep(0.05)
                return
            except Exception:
                time.sleep(0.15)
    js_utils.raise_unable_to_load_jquery_exception(driver)


def is_introjs_activated(driver):
    verify_script = """// Verify IntroJS activated
                     var intro2 = introJs();
                     """
    try:
        driver.execute_script(verify_script)
        return True
    except Exception:
        return False


def activate_shepherd(driver):
    """Allows you to use Shepherd Tours with SeleniumBase
    https://cdnjs.com/libraries/shepherd/1.8.1
    """
    shepherd_js = constants.Shepherd.MIN_JS
    sh_theme_arrows_css = constants.Shepherd.THEME_ARROWS_CSS
    sh_theme_arrows_fix_css = constants.Shepherd.THEME_ARR_FIX_CSS
    sh_theme_default_css = constants.Shepherd.THEME_DEFAULT_CSS
    sh_theme_dark_css = constants.Shepherd.THEME_DARK_CSS
    sh_theme_sq_css = constants.Shepherd.THEME_SQ_CSS
    sh_theme_sq_dark_css = constants.Shepherd.THEME_SQ_DK_CSS
    tether_js = constants.Tether.MIN_JS
    spinner_css = constants.Messenger.SPINNER_CSS
    sh_style = style_sheet.sh_style_test
    backdrop_style = style_sheet.sh_backdrop_style

    activate_bootstrap(driver)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    js_utils.add_css_style(driver, backdrop_style)
    js_utils.wait_for_ready_state_complete(driver)
    js_utils.wait_for_angularjs(driver)
    for x in range(4):
        js_utils.add_css_link(driver, spinner_css)
        js_utils.add_css_link(driver, sh_theme_arrows_css)
        js_utils.add_css_link(driver, sh_theme_arrows_fix_css)
        js_utils.add_css_link(driver, sh_theme_default_css)
        js_utils.add_css_link(driver, sh_theme_dark_css)
        js_utils.add_css_link(driver, sh_theme_sq_css)
        js_utils.add_css_link(driver, sh_theme_sq_dark_css)
        js_utils.add_js_link(driver, tether_js)
        js_utils.add_js_link(driver, shepherd_js)
        time.sleep(0.1)
        for x in range(int(settings.MINI_TIMEOUT * 2.0)):
            # Shepherd needs a small amount of time to load & activate.
            try:
                driver.execute_script(sh_style)  # Verify Shepherd has loaded
                js_utils.wait_for_ready_state_complete(driver)
                js_utils.wait_for_angularjs(driver)
                driver.execute_script(sh_style)  # Need it twice for ordering
                js_utils.wait_for_ready_state_complete(driver)
                js_utils.wait_for_angularjs(driver)
                time.sleep(0.05)
                return
            except Exception:
                time.sleep(0.15)
    js_utils.raise_unable_to_load_jquery_exception(driver)


def is_shepherd_activated(driver):
    sh_style = style_sheet.sh_style_test
    try:
        driver.execute_script(sh_style)  # Verify Shepherd has loaded
        return True
    except Exception:
        return False


def play_shepherd_tour(driver, tour_steps, msg_dur, name=None, interval=0):
    """ Plays a Shepherd tour on the current website. """
    instructions = ""
    for tour_step in tour_steps[name]:
        instructions += tour_step
    instructions += """
        // Start the tour
        tour.start();
        $tour = tour;"""
    autoplay = False
    if interval and interval > 0:
        autoplay = True
        interval = float(interval)
        if interval < 0.5:
            interval = 0.5

    if not is_shepherd_activated(driver):
        activate_shepherd(driver)

    if len(tour_steps[name]) > 1:
        try:
            selector = re.search(
                r"[\S\s]+{element: '([\S\s]+)', on: [\S\s]+",
                tour_steps[name][1],
            ).group(1)
            selector = selector.replace("\\", "")
            page_actions.wait_for_element_present(
                driver,
                selector,
                by=By.CSS_SELECTOR,
                timeout=settings.SMALL_TIMEOUT,
            )
        except Exception:
            js_utils.post_messenger_error_message(
                driver, "Tour Error: {'%s'} was not found!" % selector, msg_dur
            )
            raise Exception(
                "Tour Error: {'%s'} was not found! "
                "Exiting due to failure on first tour step!"
                "" % selector
            )
    driver.execute_script(instructions)
    tour_on = True
    if autoplay:
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (interval * 1000.0)
        latest_element = None
        latest_text = None
    while tour_on:
        try:
            time.sleep(0.01)
            result = driver.execute_script(
                "return Shepherd.activeTour.currentStep.isOpen()"
            )
        except Exception:
            tour_on = False
            result = None
        if result:
            tour_on = True
            if autoplay:
                try:
                    element = driver.execute_script(
                        "return Shepherd.activeTour.currentStep"
                        ".options.attachTo.element"
                    )
                    shep_text = driver.execute_script(
                        "return Shepherd.activeTour.currentStep"
                        ".options.text"
                    )
                except Exception:
                    continue
                if element != latest_element or shep_text != latest_text:
                    latest_element = element
                    latest_text = shep_text
                    start_ms = time.time() * 1000.0
                    stop_ms = start_ms + (interval * 1000.0)
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    if (element == latest_element) and (
                        shep_text == latest_text
                    ):
                        driver.execute_script("Shepherd.activeTour.next()")
                        try:
                            latest_element = driver.execute_script(
                                "return Shepherd.activeTour.currentStep"
                                ".options.attachTo.element"
                            )
                            latest_text = driver.execute_script(
                                "return Shepherd.activeTour.currentStep"
                                ".options.text"
                            )
                            start_ms = time.time() * 1000.0
                            stop_ms = start_ms + (interval * 1000.0)
                        except Exception:
                            pass
                        continue
        else:
            try:
                time.sleep(0.01)
                selector = driver.execute_script(
                    "return Shepherd.activeTour"
                    ".currentStep.options.attachTo.element"
                )
                try:
                    js_utils.wait_for_css_query_selector(
                        driver, selector, timeout=settings.SMALL_TIMEOUT
                    )
                except Exception:
                    remove_script = (
                        "jQuery('%s').remove()" % "div.shepherd-content"
                    )
                    driver.execute_script(remove_script)
                    js_utils.post_messenger_error_message(
                        driver,
                        "Tour Error: {'%s'} was not found!" % selector,
                        msg_dur,
                    )
                    time.sleep(0.1)
                driver.execute_script("Shepherd.activeTour.next()")
                if autoplay:
                    start_ms = time.time() * 1000.0
                    stop_ms = start_ms + (interval * 1000.0)
                tour_on = True
            except Exception:
                tour_on = False
                time.sleep(0.1)


def play_bootstrap_tour(
    driver, tour_steps, browser, msg_dur, name=None, interval=0
):
    """ Plays a Bootstrap tour on the current website. """
    instructions = ""
    for tour_step in tour_steps[name]:
        instructions += tour_step
    instructions += """]);
        // Initialize the tour
        tour.init();
        // Start the tour
        tour.start();
        // Fix timing issue by restarting tour immediately
        tour.restart();
        // Save for later
        $tour = tour;"""

    if interval and interval > 0:
        if interval < 1:
            interval = 1
        interval = str(float(interval) * 1000.0)
        instructions = instructions.replace(
            "duration: 0,", "duration: %s," % interval
        )

    if not is_bootstrap_activated(driver):
        activate_bootstrap(driver)

    if len(tour_steps[name]) > 1:
        try:
            if "element: " in tour_steps[name][1]:
                selector = re.search(
                    r"[\S\s]+element: '([\S\s]+)',[\S\s]+title: '",
                    tour_steps[name][1],
                ).group(1)
                selector = selector.replace("\\", "").replace(":first", "")
                page_actions.wait_for_element_present(
                    driver,
                    selector,
                    by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT,
                )
            else:
                selector = "html"
        except Exception:
            js_utils.post_messenger_error_message(
                driver, "Tour Error: {'%s'} was not found!" % selector, msg_dur
            )
            raise Exception(
                "Tour Error: {'%s'} was not found! "
                "Exiting due to failure on first tour step!"
                "" % selector
            )

    driver.execute_script(instructions)
    tour_on = True
    while tour_on:
        try:
            time.sleep(0.01)
            if browser != "firefox":
                result = driver.execute_script("return $tour.ended()")
            else:
                page_actions.wait_for_element_present(
                    driver, ".tour-tour", by=By.CSS_SELECTOR, timeout=0.65
                )
                result = False
        except Exception:
            tour_on = False
            result = None
        if result is False:
            tour_on = True
            time.sleep(0.05)
        else:
            try:
                time.sleep(0.01)
                if browser != "firefox":
                    result = driver.execute_script("return $tour.ended()")
                else:
                    page_actions.wait_for_element_present(
                        driver, ".tour-tour", by=By.CSS_SELECTOR, timeout=0.65
                    )
                    result = False
                if result is False:
                    time.sleep(0.05)
                    continue
                else:
                    return
            except Exception:
                tour_on = False
                time.sleep(0.1)


def play_driverjs_tour(
    driver, tour_steps, browser, msg_dur, name=None, interval=0
):
    """ Plays a DriverJS tour on the current website. """
    instructions = ""
    for tour_step in tour_steps[name]:
        instructions += tour_step
    instructions += """]
        );
        // Start the tour!
        tour.start();
        $tour = tour;"""
    autoplay = False
    if interval and interval > 0:
        autoplay = True
        interval = float(interval)
        if interval < 0.5:
            interval = 0.5

    if not is_driverjs_activated(driver):
        activate_driverjs(driver)

    if len(tour_steps[name]) > 1:
        try:
            if "element: " in tour_steps[name][1]:
                selector = re.search(
                    r"[\S\s]+element: '([\S\s]+)',[\S\s]+popover: {",
                    tour_steps[name][1],
                ).group(1)
                selector = selector.replace("\\", "").replace(":first", "")
                page_actions.wait_for_element_present(
                    driver,
                    selector,
                    by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT,
                )
            else:
                selector = "html"
        except Exception:
            js_utils.post_messenger_error_message(
                driver, "Tour Error: {'%s'} was not found!" % selector, msg_dur
            )
            raise Exception(
                "Tour Error: {'%s'} was not found! "
                "Exiting due to failure on first tour step!"
                "" % selector
            )

    driver.execute_script(instructions)
    driver.execute_script(
        'document.querySelector(".driver-next-btn").focus();'
    )
    tour_on = True
    if autoplay:
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (interval * 1000.0)
        latest_step = 0
    while tour_on:
        try:
            time.sleep(0.01)
            if browser != "firefox":
                result = not driver.execute_script("return $tour.isActivated")
            else:
                page_actions.wait_for_element_visible(
                    driver,
                    "#driver-popover-item",
                    by=By.CSS_SELECTOR,
                    timeout=1.1,
                )
                result = False
        except Exception:
            tour_on = False
            result = None
        if result is False:
            tour_on = True
            driver.execute_script(
                'document.querySelector(".driver-next-btn").focus();'
            )
            if autoplay:
                try:
                    current_step = driver.execute_script(
                        "return $tour.currentStep"
                    )
                except Exception:
                    continue
                if current_step != latest_step:
                    latest_step = current_step
                    start_ms = time.time() * 1000.0
                    stop_ms = start_ms + (interval * 1000.0)
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    if current_step == latest_step:
                        driver.execute_script("$tour.moveNext()")
                        try:
                            latest_step = driver.execute_script(
                                "return $tour.currentStep"
                            )
                            start_ms = time.time() * 1000.0
                            stop_ms = start_ms + (interval * 1000.0)
                        except Exception:
                            pass
                        continue
        else:
            try:
                time.sleep(0.01)
                if browser != "firefox":
                    result = not driver.execute_script(
                        "return $tour.isActivated"
                    )
                else:
                    page_actions.wait_for_element_visible(
                        driver,
                        "#driver-popover-item",
                        by=By.CSS_SELECTOR,
                        timeout=1.1,
                    )
                    result = False
                if result is False:
                    time.sleep(0.1)
                    continue
                else:
                    return
            except Exception:
                tour_on = False
                time.sleep(0.1)


def play_hopscotch_tour(
    driver, tour_steps, browser, msg_dur, name=None, interval=0
):
    """ Plays a Hopscotch tour on the current website. """
    instructions = ""
    for tour_step in tour_steps[name]:
        instructions += tour_step
    instructions += """]
        };
        // Start the tour!
        hopscotch.startTour(tour);
        $tour = hopscotch;"""
    autoplay = False
    if interval and interval > 0:
        autoplay = True
        interval = float(interval)
        if interval < 0.5:
            interval = 0.5

    if not is_hopscotch_activated(driver):
        activate_hopscotch(driver)

    if len(tour_steps[name]) > 1:
        try:
            if "target: " in tour_steps[name][1]:
                selector = re.search(
                    r"[\S\s]+target: '([\S\s]+)',[\S\s]+title: '",
                    tour_steps[name][1],
                ).group(1)
                selector = selector.replace("\\", "").replace(":first", "")
                page_actions.wait_for_element_present(
                    driver,
                    selector,
                    by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT,
                )
            else:
                selector = "html"
        except Exception:
            js_utils.post_messenger_error_message(
                driver, "Tour Error: {'%s'} was not found!" % selector, msg_dur
            )
            raise Exception(
                "Tour Error: {'%s'} was not found! "
                "Exiting due to failure on first tour step!"
                "" % selector
            )

    driver.execute_script(instructions)
    tour_on = True
    if autoplay:
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (interval * 1000.0)
        latest_step = 0
    while tour_on:
        try:
            time.sleep(0.01)
            if browser != "firefox":
                result = not driver.execute_script("return $tour.isActive")
            else:
                page_actions.wait_for_element_present(
                    driver,
                    ".hopscotch-bubble",
                    by=By.CSS_SELECTOR,
                    timeout=0.4,
                )
                result = False
        except Exception:
            tour_on = False
            result = None
        if result is False:
            tour_on = True
            if autoplay:
                try:
                    current_step = driver.execute_script(
                        "return $tour.getCurrStepNum()"
                    )
                except Exception:
                    continue
                if current_step != latest_step:
                    latest_step = current_step
                    start_ms = time.time() * 1000.0
                    stop_ms = start_ms + (interval * 1000.0)
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    if current_step == latest_step:
                        driver.execute_script("$tour.nextStep()")
                        try:
                            latest_step = driver.execute_script(
                                "return $tour.getCurrStepNum()"
                            )
                            start_ms = time.time() * 1000.0
                            stop_ms = start_ms + (interval * 1000.0)
                        except Exception:
                            pass
                        continue
        else:
            try:
                time.sleep(0.01)
                if browser != "firefox":
                    result = not driver.execute_script("return $tour.isActive")
                else:
                    page_actions.wait_for_element_present(
                        driver,
                        ".hopscotch-bubble",
                        by=By.CSS_SELECTOR,
                        timeout=0.4,
                    )
                    result = False
                if result is False:
                    time.sleep(0.1)
                    continue
                else:
                    return
            except Exception:
                tour_on = False
                time.sleep(0.1)


def play_introjs_tour(
    driver, tour_steps, browser, msg_dur, name=None, interval=0
):
    """ Plays an IntroJS tour on the current website. """
    instructions = ""
    for tour_step in tour_steps[name]:
        instructions += tour_step
    instructions += """]
        });
        intro.setOption("disableInteraction", true);
        intro.setOption("overlayOpacity", .29);
        intro.setOption("scrollToElement", true);
        intro.setOption("keyboardNavigation", true);
        intro.setOption("exitOnEsc", true);
        intro.setOption("hidePrev", true);
        intro.setOption("nextToDone", true);
        intro.setOption("exitOnOverlayClick", false);
        intro.setOption("showStepNumbers", false);
        intro.setOption("showProgress", false);
        intro.start();
        $tour = intro;
        };
        // Start the tour
        startIntro();
        """
    autoplay = False
    if interval and interval > 0:
        autoplay = True
        interval = float(interval)
        if interval < 0.5:
            interval = 0.5

    if not is_introjs_activated(driver):
        activate_introjs(driver)

    if len(tour_steps[name]) > 1:
        try:
            if "element: " in tour_steps[name][1]:
                selector = re.search(
                    r"[\S\s]+element: '([\S\s]+)',[\S\s]+intro: '",
                    tour_steps[name][1],
                ).group(1)
                selector = selector.replace("\\", "")
                page_actions.wait_for_element_present(
                    driver,
                    selector,
                    by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT,
                )
            else:
                selector = "html"
        except Exception:
            js_utils.post_messenger_error_message(
                driver, "Tour Error: {'%s'} was not found!" % selector, msg_dur
            )
            raise Exception(
                "Tour Error: {'%s'} was not found! "
                "Exiting due to failure on first tour step!"
                "" % selector
            )
    driver.execute_script(instructions)
    tour_on = True
    if autoplay:
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (interval * 1000.0)
        latest_step = 0
    while tour_on:
        try:
            time.sleep(0.01)
            if browser != "firefox":
                result = driver.execute_script("return $tour._currentStep")
            else:
                page_actions.wait_for_element_present(
                    driver, ".introjs-tooltip", by=By.CSS_SELECTOR, timeout=0.4
                )
                result = True
        except Exception:
            tour_on = False
            result = None
        if result is not None:
            tour_on = True
            if autoplay:
                try:
                    current_step = driver.execute_script(
                        "return $tour._currentStep"
                    )
                except Exception:
                    continue
                if current_step != latest_step:
                    latest_step = current_step
                    start_ms = time.time() * 1000.0
                    stop_ms = start_ms + (interval * 1000.0)
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    if current_step == latest_step:
                        try:
                            driver.execute_script("$tour.nextStep()")
                        except Exception:
                            driver.execute_script("$tour.exit()")
                        try:
                            latest_step = driver.execute_script(
                                "return $tour._currentStep"
                            )
                            start_ms = time.time() * 1000.0
                            stop_ms = start_ms + (interval * 1000.0)
                        except Exception:
                            pass
                        continue
        else:
            try:
                time.sleep(0.01)
                if browser != "firefox":
                    result = driver.execute_script("return $tour._currentStep")
                else:
                    page_actions.wait_for_element_present(
                        driver,
                        ".introjs-tooltip",
                        by=By.CSS_SELECTOR,
                        timeout=0.4,
                    )
                    result = True
                if result is not None:
                    time.sleep(0.1)
                    continue
                else:
                    return
            except Exception:
                tour_on = False
                time.sleep(0.1)


def export_tour(tour_steps, name=None, filename="my_tour.js", url=None):
    """Exports a tour as a JS file.
    It will include necessary resources as well, such as jQuery.
    You'll be able to copy the tour directly into the Console of
    any web browser to play the tour outside of SeleniumBase runs."""
    if not name:
        name = "default"
    if name not in tour_steps:
        raise Exception("Tour {%s} does not exist!" % name)
    if not filename.endswith(".js"):
        raise Exception('Tour file must end in ".js"!')
    if not url:
        url = "data:,"

    tour_type = None
    if "Bootstrap" in tour_steps[name][0]:
        tour_type = "bootstrap"
    elif "DriverJS" in tour_steps[name][0]:
        tour_type = "driverjs"
    elif "Hopscotch" in tour_steps[name][0]:
        tour_type = "hopscotch"
    elif "IntroJS" in tour_steps[name][0]:
        tour_type = "introjs"
    elif "Shepherd" in tour_steps[name][0]:
        tour_type = "shepherd"
    else:
        raise Exception("Unknown tour type!")

    instructions = (
        """////////  Load Tour Start Page (if not there now)  ////////\n\n"""
        """if (window.location.href != "%s") {\n"""
        """    window.location.href="%s";\n"""
        """}\n\n"""
        """////////  Resources  ////////\n\n"""
        """function injectCSS(css_link) {"""
        """var head = document.getElementsByTagName("head")[0];"""
        """var link = document.createElement("link");"""
        """link.rel = "stylesheet";"""
        """link.type = "text/css";"""
        """link.href = css_link;"""
        """link.crossorigin = "anonymous";"""
        """head.appendChild(link);"""
        """};\n"""
        """function injectJS(js_link) {"""
        """var head = document.getElementsByTagName("head")[0];"""
        """var script = document.createElement("script");"""
        """script.src = js_link;"""
        """script.defer;"""
        """script.type="text/javascript";"""
        """script.crossorigin = "anonymous";"""
        """script.onload = function() { null };"""
        """head.appendChild(script);"""
        """};\n"""
        """function injectStyle(css) {"""
        """var head = document.getElementsByTagName("head")[0];"""
        """var style = document.createElement("style");"""
        """style.type = "text/css";"""
        """style.appendChild(document.createTextNode(css));"""
        """head.appendChild(style);"""
        """};\n""" % (url, url)
    )

    if tour_type == "bootstrap":
        jquery_js = constants.JQuery.MIN_JS
        bootstrap_tour_css = constants.BootstrapTour.MIN_CSS
        bootstrap_tour_js = constants.BootstrapTour.MIN_JS
        backdrop_style = style_sheet.bt_backdrop_style
        backdrop_style = backdrop_style.replace("\n", "")
        backdrop_style = js_utils.escape_quotes_if_needed(backdrop_style)
        instructions += 'injectJS("%s");\n' % jquery_js
        instructions += "\n"
        instructions += "function loadResources() { "
        instructions += 'if ( typeof jQuery !== "undefined" ) {\n'
        instructions += 'injectCSS("%s");\n' % bootstrap_tour_css
        instructions += 'injectStyle("%s");\n' % backdrop_style
        instructions += 'injectJS("%s");' % bootstrap_tour_js
        instructions += '} else { window.setTimeout("loadResources();",100); '
        instructions += "} }\n"
        instructions += "loadResources()"

    elif tour_type == "driverjs":
        driverjs_css = constants.DriverJS.MIN_CSS
        driverjs_js = constants.DriverJS.MIN_JS
        backdrop_style = style_sheet.dt_backdrop_style
        backdrop_style = backdrop_style.replace("\n", "")
        backdrop_style = js_utils.escape_quotes_if_needed(backdrop_style)
        instructions += 'injectCSS("%s");\n' % driverjs_css
        instructions += 'injectStyle("%s");\n' % backdrop_style
        instructions += 'injectJS("%s");' % driverjs_js

    elif tour_type == "hopscotch":
        hopscotch_css = constants.Hopscotch.MIN_CSS
        hopscotch_js = constants.Hopscotch.MIN_JS
        backdrop_style = style_sheet.hops_backdrop_style
        backdrop_style = backdrop_style.replace("\n", "")
        backdrop_style = js_utils.escape_quotes_if_needed(backdrop_style)
        instructions += 'injectCSS("%s");\n' % hopscotch_css
        instructions += 'injectStyle("%s");\n' % backdrop_style
        instructions += 'injectJS("%s");' % hopscotch_js

    elif tour_type == "introjs":
        intro_css = constants.IntroJS.MIN_CSS
        intro_js = constants.IntroJS.MIN_JS
        theme_color = sb_config.introjs_theme_color
        hover_color = sb_config.introjs_hover_color
        backdrop_style = style_sheet.introjs_style % (
            theme_color,
            hover_color,
            hover_color,
            hover_color,
            theme_color,
        )
        backdrop_style = backdrop_style.replace("\n", "")
        backdrop_style = js_utils.escape_quotes_if_needed(backdrop_style)
        instructions += 'injectCSS("%s");\n' % intro_css
        instructions += 'injectStyle("%s");\n' % backdrop_style
        instructions += 'injectJS("%s");' % intro_js

    elif tour_type == "shepherd":
        jquery_js = constants.JQuery.MIN_JS
        shepherd_js = constants.Shepherd.MIN_JS
        sh_theme_arrows_css = constants.Shepherd.THEME_ARROWS_CSS
        sh_theme_arrows_fix_css = constants.Shepherd.THEME_ARR_FIX_CSS
        sh_theme_default_css = constants.Shepherd.THEME_DEFAULT_CSS
        sh_theme_dark_css = constants.Shepherd.THEME_DARK_CSS
        sh_theme_sq_css = constants.Shepherd.THEME_SQ_CSS
        sh_theme_sq_dark_css = constants.Shepherd.THEME_SQ_DK_CSS
        tether_js = constants.Tether.MIN_JS
        spinner_css = constants.Messenger.SPINNER_CSS
        backdrop_style = style_sheet.sh_backdrop_style
        backdrop_style = backdrop_style.replace("\n", "")
        backdrop_style = js_utils.escape_quotes_if_needed(backdrop_style)
        instructions += 'injectCSS("%s");\n' % spinner_css
        instructions += 'injectJS("%s");\n' % jquery_js
        instructions += 'injectJS("%s");\n' % tether_js
        instructions += "\n"
        instructions += "function loadResources() { "
        instructions += 'if ( typeof jQuery !== "undefined" ) {\n'
        instructions += 'injectCSS("%s");' % sh_theme_arrows_css
        instructions += 'injectCSS("%s");' % sh_theme_arrows_fix_css
        instructions += 'injectCSS("%s");' % sh_theme_default_css
        instructions += 'injectCSS("%s");' % sh_theme_dark_css
        instructions += 'injectCSS("%s");' % sh_theme_sq_css
        instructions += 'injectCSS("%s");\n' % sh_theme_sq_dark_css
        instructions += 'injectStyle("%s");\n' % backdrop_style
        instructions += 'injectJS("%s");\n' % shepherd_js
        instructions += '} else { window.setTimeout("loadResources();",100); '
        instructions += "} }\n"
        instructions += "loadResources()"

    instructions += "\n\n////////  Tour Code  ////////\n\n"
    if tour_type == "bootstrap":
        instructions += "function loadTour() { "
        instructions += 'if ( typeof Tour !== "undefined" ) {\n'
    elif tour_type == "driverjs":
        instructions += "function loadTour() { "
        instructions += 'if ( typeof Driver !== "undefined" ) {\n'
    elif tour_type == "hopscotch":
        instructions += "function loadTour() { "
        instructions += 'if ( typeof hopscotch !== "undefined" ) {\n'
    elif tour_type == "introjs":
        instructions += "function loadTour() { "
        instructions += 'if ( typeof introJs !== "undefined" ) {\n'
    elif tour_type == "shepherd":
        instructions += "function loadTour() { "
        instructions += 'if ( typeof Shepherd !== "undefined" ) {\n'

    for tour_step in tour_steps[name]:
        instructions += tour_step

    if tour_type == "bootstrap":
        instructions += """]);
            // Initialize the tour
            tour.init();
            // Start the tour
            tour.start();
            $tour = tour;
            $tour.restart();\n"""
    elif tour_type == "driverjs":
        instructions += """]
            );
            // Start the tour!
            tour.start();
            $tour = tour;\n"""
    elif tour_type == "hopscotch":
        instructions += """]
            };
            // Start the tour!
            hopscotch.startTour(tour);
            $tour = hopscotch;\n"""
    elif tour_type == "introjs":
        instructions += """]
            });
            intro.setOption("disableInteraction", true);
            intro.setOption("overlayOpacity", .29);
            intro.setOption("scrollToElement", true);
            intro.setOption("keyboardNavigation", true);
            intro.setOption("exitOnEsc", true);
            intro.setOption("hidePrev", true);
            intro.setOption("nextToDone", true);
            intro.setOption("exitOnOverlayClick", false);
            intro.setOption("showStepNumbers", false);
            intro.setOption("showProgress", false);
            intro.start();
            $tour = intro;
            };
            startIntro();\n"""
    elif tour_type == "shepherd":
        instructions += """
            tour.start();
            $tour = tour;\n"""
    else:
        pass
    instructions += '\n} else { window.setTimeout("loadTour();",100); } '
    instructions += "}\n"
    instructions += "loadTour()\n"

    exported_tours_folder = EXPORTED_TOURS_FOLDER
    if exported_tours_folder.endswith("/"):
        exported_tours_folder = exported_tours_folder[:-1]
    if not os.path.exists(exported_tours_folder):
        try:
            os.makedirs(exported_tours_folder)
        except Exception:
            pass
    import codecs

    file_path = exported_tours_folder + "/" + filename
    out_file = codecs.open(file_path, "w+", encoding="utf-8")
    out_file.writelines(instructions)
    out_file.close()
    print("\n>>> [%s] was saved!\n" % file_path)
