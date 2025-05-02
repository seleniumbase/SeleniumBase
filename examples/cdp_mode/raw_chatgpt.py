from contextlib import suppress
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://chatgpt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.click_if_visible('button[aria-label="Close dialog"]')
    sb.click_if_visible('button[data-testid="close-button"]')
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
