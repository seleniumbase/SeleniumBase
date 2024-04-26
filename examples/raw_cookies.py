"""A SeleniumBase test that loads cookies to bypass login."""
from seleniumbase import SB

# Log in to Swag Labs and save cookies
with SB(test=True) as sb:
    sb.open("https://www.saucedemo.com")
    sb.wait_for_element("div.login_logo")
    sb.type("#user-name", "standard_user")
    sb.type("#password", "secret_sauce")
    sb.click('input[type="submit"]')
    sb.highlight("div.inventory_list", loops=6)
    sb.save_cookies(name="cookies.txt")

# Load previously saved cookies to bypass login
with SB(test=True) as sb:
    sb.open("https://www.saucedemo.com")
    sb.load_cookies(name="cookies.txt")
    sb.open("https://www.saucedemo.com/inventory.html")
    sb.highlight("div.inventory_list", loops=12)
