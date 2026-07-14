from contextlib import suppress
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    sb.activate_cdp_mode()
    sb.open("https://chatgpt.com/")
    sb.sleep(1)
    close_1 = 'button[aria-label="Close dialog"]'
    close_2 = 'button[data-testid="close-button"]'
    sb.click_if_visible("%s, %s" % (close_1, close_2))
    query = "Compare Playwright to SeleniumBase in under 178 words"
    sb.press_keys("#prompt-textarea", query)
    sb.click('button[data-testid="send-button"]')
    print('*** Input for ChatGPT: ***\n"%s"' % query)
    sb.sleep(3)
    with suppress(Exception):
        # The "Stop" button disappears when ChatGPT is done typing a response
        sb.wait_for_element_not_visible(
            'button[data-testid="stop-button"]', timeout=20
        )
    chat = sb.find_element('[data-message-author-role="assistant"] .markdown')
    soup = sb.get_beautiful_soup(chat.get_html()).text.strip()
    soup = soup.replace("\n\n\n", "\n\n")
    print("*** Response from ChatGPT: ***\n%s" % soup)
    sb.sleep(3)
