from behave import step


@step("Open the Fail Page")
def go_to_error_page(context):
    context.sb.open("https://seleniumbase.io/error_page/")


@step("Fail test on purpose")
def fail_on_purpose(context):
    context.sb.fail("This test fails on purpose!")
