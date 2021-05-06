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
    result = testdir.inline_run("--headless", "--rs")
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
    result = testdir.inline_run("--headless")
    assert result.matchreport("test_basecase").passed


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
    result = testdir.inline_run("--headless")
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
    result = testdir.inline_run("--headless")
    assert result.matchreport("test_request_sb_fixture").passed
