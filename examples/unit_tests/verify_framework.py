""" Run with pytest """


def test_simple_cases(testdir):
    """Verify a simple passing test and a simple failing test.
    The failing test is marked as xfail to have it skipped."""
    testdir.makepyfile(
        """
        import pytest
        from seleniumbase import BaseCase
        class MyTestCase(BaseCase):
            def test_passing(self):
                self.assert_equal('yes', 'yes')
            @pytest.mark.xfail
            def test_failing(self):
                self.assert_equal('yes', 'no')
        """
    )
    result = testdir.inline_run("--headless", "--rs", "-v")
    assert result.matchreport("test_passing").passed
    assert result.matchreport("test_failing").skipped


def test_basecase(testdir):
    testdir.makepyfile(
        """
        from seleniumbase import BaseCase
        class MyTest(BaseCase):
            def test_basecase(self):
                self.open("data:text/html,<p>Hello<br><input></p>")
                self.assert_element("html > body")  # selector
                self.assert_text("Hello", "body p")  # text, selector
                self.type("input", "Goodbye")  # selector, text
                self.click("body p")  # selector
        """
    )
    result = testdir.inline_run("--headless", "-v")
    assert result.matchreport("test_basecase").passed


def test_run_with_dashboard(testdir):
    testdir.makepyfile(
        """
        from seleniumbase import BaseCase
        class MyTestCase(BaseCase):
            def test_1_passing(self):
                self.assert_equal('yes', 'yes')
            def test_2_failing(self):
                self.assert_equal('yes', 'no')
            def test_3_skipped(self):
                self.skip("Skip!")
        """
    )
    result = testdir.inline_run("--headless", "--rs", "--dashboard", "-v")
    assert result.matchreport("test_1_passing").passed
    assert result.matchreport("test_2_failing").failed
    assert result.matchreport("test_3_skipped").skipped


def test_sb_fixture(testdir):
    testdir.makepyfile(
        """
        def test_sb_fixture(sb):
            sb.open("data:text/html,<p>Hello<br><input></p>")
            sb.assert_element("html > body")  # selector
            sb.assert_text("Hello", "body p")  # text, selector
            sb.type("input", "Goodbye")  # selector, text
            sb.click("body p")  # selector
        """
    )
    result = testdir.inline_run("--headless", "-v")
    assert result.matchreport("test_sb_fixture").passed


def test_request_sb_fixture(testdir):
    testdir.makepyfile(
        """
        def test_request_sb_fixture(request):
            sb = request.getfixturevalue('sb')
            sb.open("data:text/html,<p>Hello<br><input></p>")
            sb.assert_element("html > body")  # selector
            sb.assert_text("Hello", "body p")  # text, selector
            sb.type("input", "Goodbye")  # selector, text
            sb.click("body p")  # selector
            sb.tearDown()
        """
    )
    result = testdir.inline_run("--headless", "-v")
    assert result.matchreport("test_request_sb_fixture").passed


def check_outcome_field(outcomes, field_name, expected_value):
    field_value = outcomes.get(field_name, 0)
    assert field_value == expected_value, (
        "outcomes.%s has an unexpected value! "
        'Expected "%s" but got "%s"!'
        % (field_name, expected_value, field_value)
    )


def assert_outcomes(
    result,
    passed=1,
    skipped=0,
    failed=0,
    xfailed=0,
    xpassed=0,
    rerun=0,
):
    outcomes = result.parseoutcomes()
    check_outcome_field(outcomes, "passed", passed)
    check_outcome_field(outcomes, "skipped", skipped)
    check_outcome_field(outcomes, "failed", failed)
    check_outcome_field(outcomes, "xfailed", xfailed)
    check_outcome_field(outcomes, "xpassed", xpassed)
    check_outcome_field(outcomes, "rerun", rerun)


def test_rerun_failures(testdir):
    testdir.makepyfile(
        """
        from seleniumbase import BaseCase
        class MyTestCase(BaseCase):
            def test_passing(self):
                self.assert_equal('yes', 'yes')
            def test_failing(self):
                self.assert_equal('yes', 'no')
        """
    )
    result = testdir.runpytest("--headless", "--reruns=1", "--rs", "-v")
    assert_outcomes(result, passed=1, failed=1, rerun=1)


def test_browser_launcher(testdir):
    testdir.makepyfile(
        """
        from seleniumbase import get_driver
        def test_browser_launcher():
            success = False
            try:
                driver = get_driver("chrome", headless=True)
                driver.get("data:text/html,<p>Data URL</p>")
                source = driver.page_source
                assert "Data URL" in source
                success = True  # No errors
            finally:
                driver.quit()
            assert success
        """
    )
    result = testdir.inline_run("--headless", "-v")
    assert result.matchreport("test_browser_launcher").passed


def test_framework_components(testdir):
    testdir.makepyfile(
        """
        from seleniumbase import get_driver
        from seleniumbase import js_utils
        from seleniumbase import page_actions
        def test_framework_components():
            success = False
            try:
                driver = get_driver("chrome", headless=True)
                driver.get('data:text/html,<h1 class="top">Data URL</h2>')
                source = driver.page_source
                assert "Data URL" in source
                assert page_actions.is_element_visible(driver, "h1.top")
                js_utils.highlight_with_js(driver, "h1.top", 2, "")
                success = True  # No errors
            finally:
                driver.quit()
            assert success
        """
    )
    result = testdir.inline_run("--headless", "-v")
    assert result.matchreport("test_framework_components").passed
