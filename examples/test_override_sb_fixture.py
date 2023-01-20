"""Overriding the "sb" fixture to override the driver."""
import pytest


@pytest.fixture()
def sb(request):
    from selenium import webdriver
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def get_new_driver(self, *args, **kwargs):
            """This method overrides get_new_driver() from BaseCase."""
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"],
            )
            return webdriver.Chrome(options=options)

        def setUp(self):
            super().setUp()

        def base_method(self):
            pass

        def tearDown(self):
            self.save_teardown_screenshot()
            super().tearDown()

    sb = BaseClass("base_method")
    sb.setUpClass()
    sb.setUp()
    yield sb
    sb.tearDown()
    sb.tearDownClass()


def test_override_fixture_no_class(sb):
    sb.open("https://seleniumbase.io/demo_page")
    sb.type("#myTextInput", "This is Automated")


class TestOverride:
    def test_override_fixture_inside_class(self, sb):
        sb.open("https://seleniumbase.io/demo_page")
        sb.type("#myTextInput", "This is Automated")
