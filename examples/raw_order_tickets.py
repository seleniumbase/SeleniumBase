from seleniumbase import SB

with SB(uc=True, test=True, ad_block_on=True) as sb:
    url = "https://www.thaiticketmajor.com/concert/"
    sb.driver.uc_open_with_reconnect(url, 5.5)
    sb.driver.uc_click("button.btn-signin", 4)
    sb.switch_to_frame('iframe[title*="Cloudflare"]')
    sb.assert_element("div#success svg#success-icon")
    sb.switch_to_default_content()
    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!")
