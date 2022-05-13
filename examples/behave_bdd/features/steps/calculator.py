from behave import step


@step("Open the Calculator App")
def go_to_calculator(context):
    context.sb.open("https://seleniumbase.io/apps/calculator")


@step("Press C")
def press_c(context):
    context.sb.click("button#clear")


@step("Press (")
def press_open_paren(context):
    context.sb.click('button[id="("]')


@step("Press )")
def press_close_paren(context):
    context.sb.click('button[id=")"]')


@step("Press ÷")
def press_divide(context):
    context.sb.click("button#divide")


@step("Press ×")
def press_multiply(context):
    context.sb.click("button#multiply")


@step("Press -")
def press_subtract(context):
    context.sb.click("button#subtract")


@step("Press +")
def press_add(context):
    context.sb.click("button#add")


@step("Press =")
def press_equal(context):
    context.sb.click("button#equal")


@step("Press 1")
def press_1(context):
    context.sb.click('button[id="1"]')


@step("Press 2")
def press_2(context):
    context.sb.click('button[id="2"]')


@step("Press 3")
def press_3(context):
    context.sb.click('button[id="3"]')


@step("Press 4")
def press_4(context):
    context.sb.click('button[id="4"]')


@step("Press 5")
def press_5(context):
    context.sb.click('button[id="5"]')


@step("Press 6")
def press_6(context):
    context.sb.click('button[id="6"]')


@step("Press 7")
def press_7(context):
    context.sb.click('button[id="7"]')


@step("Press 8")
def press_8(context):
    context.sb.click('button[id="8"]')


@step("Press 9")
def press_9(context):
    context.sb.click('button[id="9"]')


@step("Press 0")
def press_0(context):
    context.sb.click('button[id="0"]')


@step("Press ←")
def press_delete(context):
    context.sb.click("button#delete")


@step("Press .")
def press_dot(context):
    context.sb.click('button[id="."]')


@step("Press [{number}]")
def enter_number_into_calc(context, number):
    sb = context.sb
    for digit in number:
        sb.click('button[id="%s"]' % digit)


@step("Evaluate [{equation}]")
def evaluate_equation(context, equation):
    sb = context.sb
    for key in equation:
        if key == " ":
            continue
        elif key == "÷":
            sb.click("button#divide")
        elif key == "×":
            sb.click("button#multiply")
        elif key == "-":
            sb.click("button#subtract")
        elif key == "+":
            sb.click("button#add")
        else:
            sb.click('button[id="%s"]' % key)
    sb.click("button#equal")


@step('Verify output is "{output}"')
def verify_output(context, output):
    sb = context.sb
    sb.assert_exact_text(output, "#output")


@step("Save calculator screenshot to logs")
def save_calculator_screenshot_to_logs(context):
    sb = context.sb
    sb.save_screenshot_to_logs()
