"""Example of using CDP Mode without WebDriver"""
import asyncio
from seleniumbase import decorators
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


@decorators.print_runtime("CDP Priceline Example")
def main():
    url0 = "about:blank"  # Set Locale code from here first
    url1 = "https://www.priceline.com/"  # (The "real" URL)
    loop = asyncio.new_event_loop()
    driver = cdp_driver.cdp_util.start_sync()
    page = loop.run_until_complete(driver.get(url0))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.set_locale("en")  # This test expects English locale
    sb.open(url1)
    sb.sleep(2.5)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(3.5)
    sb.remove_elements("msm-cookie-banner")
    sb.sleep(1.5)
    location = "Amsterdam"
    where_to = 'div[data-automation*="experiences"] input'
    button = 'button[data-automation*="experiences-search"]'
    sb.gui_click_element(where_to)
    sb.press_keys(where_to, location)
    sb.sleep(1)
    sb.gui_click_element(button)
    sb.sleep(3)
    print(sb.get_title())
    print("************")
    for i in range(8):
        sb.scroll_down(50)
        sb.sleep(0.2)
    cards = sb.select_all('h2[data-automation*="product-list-card"]')
    for card in cards:
        print("* %s" % card.text)


if __name__ == "__main__":
    main()
