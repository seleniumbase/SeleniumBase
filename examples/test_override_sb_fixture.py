"""Overriding the "sb" fixture to override the driver."""
import pytest


@pytest.fixture()
def sb(request):
    import sys
    from selenium import webdriver
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def setUp(self):
            super(BaseClass, self).setUp()

        def tearDown(self):
            self.save_teardown_screenshot()
            super(BaseClass, self).tearDown()

        def base_method(self):
            pass

        def get_new_driver(self, *args, **kwargs):
            """This method overrides get_new_driver() from BaseCase."""
            options = webdriver.ChromeOptions()
            if "linux" in sys.platform:
                options.add_argument("--headless=chrome")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"],
            )
            return webdriver.Chrome(options=options)

    if request.cls:
        request.cls.sb = BaseClass("base_method")
        request.cls.sb.setUp()
        yield request.cls.sb
        request.cls.sb.tearDown()
    else:
        sb = BaseClass("base_method")
        sb.setUp()
        yield sb
        sb.tearDown()


def test_override_fixture_no_class(sb):
    sb.open("https://seleniumbase.io/demo_page")
    sb.type("#myTextInput", "This is Automated")


class TestOverride:
    def test_override_fixture_inside_class(self, sb):
        sb.open("https://seleniumbase.io/demo_page")
        sb.type("#myTextInput", "This is Automated")
