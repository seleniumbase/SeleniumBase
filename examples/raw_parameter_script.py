""" The main purpose of this file is to demonstrate running SeleniumBase
    scripts without the use of Pytest by calling the script directly
    with Python or from a Python interactive interpreter. Based on
    whether relative imports work or don't, the script can autodetect
    how this file was run. With pure Python, it will initialize
    all the variables that would've been automatically initialized
    by the Pytest plugin. The setUp() and tearDown() methods are also
    now called from the script itself.

    One big advantage to running tests with Pytest is that most of this
    is done for you automatically, with the option to update any of the
    parameters through command line parsing. Pytest also provides you
    with other plugins, such as ones for generating test reports,
    handling multithreading, and parametrized tests. Depending on your
    specific needs, you may need to call SeleniumBase commands without
    using Pytest, and this example shows you how. """

try:
    # Running with Pytest / (Finds test methods to run using autodiscovery)
    # Example run command:  "pytest raw_parameter_script.py"
    from .my_first_test import MyTestClass  # (relative imports work: ".~")

except (ImportError, ValueError):
    # Running with pure Python OR from a Python interactive interpreter
    # Example run command:  "python raw_parameter_script.py"
    from my_first_test import MyTestClass  # (relative imports DON'T work)

    b = MyTestClass("test_basic")
    b.browser = "chrome"
    b.headless = False
    b.servername = "localhost"
    b.port = 4444
    b.data = None
    b.environment = "test"
    b.user_agent = None
    b.database_env = "test"
    b.log_path = "latest_logs/"
    b.archive_logs = False
    b.disable_csp = False
    b.visual_baseline = False
    b.save_screenshot_after_test = False
    b.timeout_multiplier = None
    b.pytest_html_report = None
    b.report_on = False
    b.with_db_reporting = False
    b.with_s3_logging = False
    b.js_checking_on = False
    b.is_pytest = False
    b.demo_mode = False
    b.demo_sleep = 1
    b.message_duration = 2
    b.proxy_string = None
    b.ad_block_on = False
    b.highlights = None
    b.check_js = False
    b.cap_file = None

    b.setUp()
    try:
        b.test_basic()
    finally:
        b.tearDown()
        del b
