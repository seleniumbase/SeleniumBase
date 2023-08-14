"""Overriding the "sb" fixture to override the driver."""
import pytest


@pytest.fixture()
def sb(request):
    from selenium import webdriver
    from seleniumbase import BaseCase
    from seleniumbase import config as sb_config

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

    if request.cls:
        request.cls.sb = BaseClass("base_method")
        request.cls.sb.setUp()
        request.cls.sb._needs_tearDown = True
        request.cls.sb._using_sb_fixture = True
        request.cls.sb._using_sb_fixture_class = True
        sb_config._sb_node[request.node.nodeid] = request.cls.sb
        yield request.cls.sb
        if request.cls.sb._needs_tearDown:
            request.cls.sb.tearDown()
            request.cls.sb._needs_tearDown = False
    else:
        sb = BaseClass("base_method")
        sb.setUp()
        sb._needs_tearDown = True
        sb._using_sb_fixture = True
        sb._using_sb_fixture_no_class = True
        sb_config._sb_node[request.node.nodeid] = sb
        yield sb
        if sb._needs_tearDown:
            sb.tearDown()
            sb._needs_tearDown = False


def test_override_fixture_no_class(sb):
    sb.open("https://seleniumbase.io/demo_page")
    sb.type("#myTextInput", "This is Automated")


class TestOverride:
    def test_override_fixture_inside_class(self, sb):
        sb.open("https://seleniumbase.io/demo_page")
        sb.type("#myTextInput", "This is Automated")
