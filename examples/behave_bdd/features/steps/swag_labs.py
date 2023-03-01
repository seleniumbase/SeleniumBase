from behave import step


@step("Open the Swag Labs Login Page")
def go_to_swag_labs(context):
    sb = context.sb
    sb.open("https://www.saucedemo.com")
    sb.clear_local_storage()


@step("Login to Swag Labs with {user}")
def login_to_swag_labs(context, user):
    sb = context.sb
    sb.type("#user-name", user)
    sb.type("#password", "secret_sauce\n")


@step("Verify that the current user is logged in")
def verify_logged_in(context):
    sb = context.sb
    sb.assert_element("#header_container")
    sb.assert_element("#react-burger-menu-btn")
    sb.assert_element("#shopping_cart_container")


@step('Add "{item}" to cart')
def add_item_to_cart(context, item):
    sb = context.sb
    sb.click('div.inventory_item:contains("%s") button[name*="add"]' % item)


@step('Save price of "{item}" to <{var}>')
def save_price_of_item(context, item, var):
    sb = context.sb
    price = sb.get_text(
        'div.inventory_item:contains("%s") .inventory_item_price' % item
    )
    sb.variables[var] = price


@step('Remove "{item}" from cart')
def remove_item_to_cart(context, item):
    sb = context.sb
    sb.click('div.inventory_item:contains("%s") button[name*="remove"]' % item)


@step("Verify shopping cart badge shows {number} item(s)")
def verify_badge_number(context, number):
    sb = context.sb
    sb.assert_exact_text(number, "span.shopping_cart_badge")


@step("Verify shopping cart badge is missing")
def verify_badge_missing(context):
    sb = context.sb
    sb.assert_element_not_visible("span.shopping_cart_badge")


@step("Click on shopping cart icon")
def click_shopping_cart(context):
    sb = context.sb
    sb.click("#shopping_cart_container a")


@step("Click Checkout")
def click_checkout(context):
    sb = context.sb
    sb.click("#checkout")


@step("Enter checkout info: {first_name}, {last_name}, {zip_code}")
def enter_checkout_info(context, first_name, last_name, zip_code):
    sb = context.sb
    sb.type("#first-name", first_name)
    sb.type("#last-name", last_name)
    sb.type("#postal-code", zip_code)


@step("Click Continue")
def click_continue(context):
    sb = context.sb
    sb.click("input#continue")


@step('Verify {quantity} "{item}"(s) in cart')
def verify_item_in_cart(context, quantity, item):
    sb = context.sb
    sb.assert_exact_text(
        quantity, 'div.cart_item:contains("%s") div.cart_quantity' % item
    )


@step('Verify cost of "{item}" is <{var}>')
def verify_cost_of_item(context, item, var):
    sb = context.sb
    earlier_price = sb.variables[var]
    sb.assert_exact_text(
        earlier_price,
        'div.cart_item_label:contains("%s") .inventory_item_price' % item,
    )


@step("Verify item total is {item_total}")
def verify_item_total(context, item_total):
    sb = context.sb
    sb.assert_exact_text(
        "Item total: %s" % item_total, "div.summary_subtotal_label", timeout=1
    )


@step("Verify tax amount is {tax_amount}")
def verify_tax_amount(context, tax_amount):
    sb = context.sb
    sb.assert_exact_text(
        "Tax: %s" % tax_amount, "div.summary_tax_label", timeout=1
    )


@step("Verify total cost is {total_cost}")
def verify_total_cost(context, total_cost):
    sb = context.sb
    sb.assert_exact_text(
        "Total: %s" % total_cost, "div.summary_total_label", timeout=1
    )


@step("Click Finish")
def click_finish(context):
    sb = context.sb
    sb.click("button#finish")


@step("Verify order complete")
def verify_order_complete(context):
    sb = context.sb
    sb.assert_exact_text("Thank you for your order!", "h2")
    sb.assert_element('img[alt="Pony Express"]')


@step("Logout from Swag Labs")
def logout_from_swag_labs(context):
    sb = context.sb
    sb.js_click("a#logout_sidebar_link")


@step("Verify on Login page")
def verify_on_login_page(context):
    sb = context.sb
    sb.assert_element("#login-button")


@step("Sort items from Z to A")
def sort_items_from_z_to_a(context):
    sb = context.sb
    sb.select_option_by_text("select.product_sort_container", "Name (Z to A)")


@step('Verify "{item}" on top')
def verify_item_on_top(context, item):
    sb = context.sb
    sb.assert_text(item, "div.inventory_item_name")
