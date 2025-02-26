"""Example of using CDP Mode with WebDriver"""
from seleniumbase import SB


with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.priceline.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.internalize_links()  # Don't open links in a new tab
    sb.click("#link_header_nav_experiences")
    sb.sleep(3.5)
    sb.remove_elements("msm-cookie-banner")
    sb.sleep(1.5)
    location = "Amsterdam"
    where_to = 'div[data-automation*="experiences"] input'
    button = 'button[data-automation*="experiences-search"]'
    sb.cdp.gui_click_element(where_to)
    sb.press_keys(where_to, location)
    sb.sleep(1)
    sb.cdp.gui_click_element(button)
    sb.sleep(3)
    print(sb.get_title())
    print("************")
    for i in range(8):
        sb.cdp.scroll_down(50)
        sb.sleep(0.2)
    cards = sb.select_all('h2[data-automation*="product-list-card"]')
    for card in cards:
        print("* %s" % card.text)
