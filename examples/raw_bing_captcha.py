from seleniumbase import SB


with SB(uc=True, test=True) as sb:
    url = "https://www.bing.com/turing/captcha/challenge"
    sb.driver.uc_open_with_tab(url)
    sb.add_css_style("iframe{zoom: 2}")  # Make it bigger
    sb.switch_to_frame("iframe")
    sb.activate_demo_mode()  # See asserts as they happen
    sb.assert_element("svg#success-icon")
    sb.assert_text("Success!", "span#success-text")
    sb.highlight("div#success", loops=8)
    sb.sleep(1)
