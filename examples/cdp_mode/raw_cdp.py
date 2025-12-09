"""Example of using CDP Mode without WebDriver"""
from seleniumbase import decorators
from seleniumbase import sb_cdp


@decorators.print_runtime("CDP Priceline Example")
def main():
    url = "https://www.priceline.com/"
    sb = sb_cdp.Chrome(url, lang="en")
    sb.sleep(2)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(3)
    sb.remove_elements("msm-cookie-banner")
    sb.sleep(1)
    location = "Amsterdam"
    where_to = 'div[data-automation*="experiences"] input'
    button = 'button[data-automation*="experiences-search"]'
    sb.wait_for_text("Where to?")
    sb.click(where_to)
    sb.press_keys(where_to, location)
    sb.sleep(1)
    sb.click(button)
    sb.sleep(2)
    sb.click_if_visible('button[aria-label="Close"]')
    sb.sleep(1)
    print(sb.get_title())
    print("************")
    for i in range(8):
        sb.scroll_down(50)
        sb.sleep(0.2)
    cards = sb.select_all('span[data-automation*="product-list-card"]')
    for card in cards:
        print("* %s" % card.text)
    sb.driver.stop()


if __name__ == "__main__":
    main()
