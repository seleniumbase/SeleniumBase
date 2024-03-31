from seleniumbase import SB


with SB(uc=True, test=True) as sb:
    url = "https://www.bing.com/turing/captcha/challenge"
    sb.driver.uc_open_with_reconnect(url, 1.25)
    sb.add_css_style("iframe{zoom: 2}")  # Make it bigger
    sb.switch_to_frame("iframe")
    if not sb.is_element_visible("div#success"):
        sb.driver.uc_open_with_reconnect(url, 4.05)
        sb.add_css_style("iframe{zoom: 2}")
        sb.switch_to_frame("iframe")
    sb.highlight("div#success", loops=2)
    sb.assert_text("Success!", "span#success-text")
    sb.activate_demo_mode()  # See asserts as they happen
    sb.assert_element("svg#success-icon")
