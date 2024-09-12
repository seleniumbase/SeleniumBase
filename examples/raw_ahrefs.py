from seleniumbase import SB

with SB(uc=True, test=True, incognito=True, locale_code="en") as sb:
    url = "https://ahrefs.com/website-authority-checker"
    input_field = 'input[placeholder="Enter domain"]'
    submit_button = 'span:contains("Check Authority")'
    sb.uc_open_with_reconnect(url)  # The bot-check is later
    sb.type(input_field, "github.com/seleniumbase/SeleniumBase")
    sb.reconnect(0.1)
    sb.uc_click(submit_button, reconnect_time=3.25)
    sb.uc_gui_click_captcha()
    sb.wait_for_text_not_visible("Checking", timeout=11.5)
    sb.highlight('p:contains("github.com/seleniumbase/SeleniumBase")')
    sb.highlight('a:contains("Top 100 backlinks")')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
