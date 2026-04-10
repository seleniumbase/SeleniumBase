from seleniumbase import SB

with SB() as sb:
    sb.open("https://www.saucedemo.com")
    sb.type("#user-name", "standard_user")
    sb.type("#password", "secret_sauce\n")
    sb.assert_element("div.inventory_list")
    sb.assert_text("Products", "span.title")

    sb.click('button[name*="backpack"]')
    sb.click("#shopping_cart_container a")
    sb.assert_exact_text("Your Cart", "span.title")
    sb.assert_text("Backpack", "div.cart_item")

    sb.click("#remove-sauce-labs-backpack")
    sb.assert_element_not_visible("div.cart_item")

    sb.click("#react-burger-menu-btn")
    sb.click("a#logout_sidebar_link")
    sb.assert_element("input#login-button")
