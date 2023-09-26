from seleniumbase import DriverContext

with DriverContext() as driver:
    driver.open("seleniumbase.io/simple/login")
    driver.type("#username", "demo_user")
    driver.type("#password", "secret_pass")
    driver.click('a:contains("Sign in")')
    driver.assert_exact_text("Welcome!", "h1")
    driver.assert_element("img#image1")
    driver.highlight("#image1")
    driver.click_link("Sign out")
    driver.assert_text("signed out", "#top_message")
