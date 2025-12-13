from seleniumbase import decorators
from seleniumbase import sb_cdp


def main():
    url = "https://seleniumbase.io/simple/login"
    sb = sb_cdp.Chrome(url)
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.click('a:contains("Sign in")')
    sb.assert_exact_text("Welcome!", "h1")
    sb.assert_element("img#image1")
    sb.highlight("#image1")
    top_nav = sb.find_element("div.topnav")
    links = top_nav.query_selector_all("a")
    for nav_item in links:
        print(nav_item.text)
    sb.click_link("Sign out")
    sb.assert_text("signed out", "#top_message")
    sb.driver.stop()


if __name__ == "__main__":
    with decorators.print_runtime("raw_cdp_login.py"):
        main()
