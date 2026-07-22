"""An example of bypassing PerimeterX detection on Priceline."""
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", guest=True, pls="none") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.priceline.com")
    sb.sleep(3)
    input_selector = "div.location-input input"
    sb.click(input_selector)
    location = "Portland, OR"
    selection = "Oregon, United States"  # (Dropdown option)
    sb.press_keys(input_selector, location)
    sb.sleep(0.5)
    sb.click(selection)
    sb.sleep(0.4)
    sb.scroll_down(25)
    sb.sleep(0.2)
    overlay_close = '[aria-label*="Overlay"] [title="Close"]'
    calendar_close = 'button[aria-label="Dismiss calendar"]'
    if not sb.is_element_visible(calendar_close):
        calendar_close = '[data-mode="range"] span.px-1'
    sb.click_if_visible(overlay_close)
    sb.sleep(0.3)
    sb.click(calendar_close)
    sb.sleep(0.3)
    sb.click_if_visible(overlay_close)
    sb.sleep(0.3)
    sb.click('form button[type="submit"]')
    sb.sleep(4.8)
    if len(sb.get_tabs()) > 1:
        sb.close_active_tab()
        sb.switch_to_newest_tab()
        sb.sleep(0.6)
    sb.sleep(0.8)
    titles = []
    count = 0
    for y in range(1, 10):
        sb.scroll_to_y(y * 500)
        hotels = sb.find_elements('div[data-vis-key*="content"]')
        for hotel in hotels:
            title = hotel.query_selector("h3")
            if title and title not in titles:
                titles.append(title)
                price = hotel.query_selector(".text-heading4")
                if price:
                    count += 1
                    price_text = price.text.replace(" ", "")
                    print("* %s: %s => %s" % (count, title.text, price_text))
    if not count:
        print("No availability over the selected dates!")
