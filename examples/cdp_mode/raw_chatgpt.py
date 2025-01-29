from contextlib import suppress
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://chatgpt.com/"
    sb.activate_cdp_mode(url)
    query = "Compare Playwright to SeleniumBase in under 178 words"
    sb.type("#prompt-textarea", query)
    sb.click('button[data-testid="send-button"]')
    print('*** Input for ChatGPT: ***\n"%s"' % query)
    with suppress(Exception):
        # The "Send" button reappears when ChatGPT is done typing a response
        sb.wait_for_element('button[data-testid="send-button"]', timeout=22)
    chat = sb.find_element('[data-message-author-role="assistant"] .markdown')
    soup = sb.get_beautiful_soup(chat.get_html()).get_text("\n").strip()
    print("*** Response from ChatGPT: ***\n%s" % soup.replace("\n:", ":"))
    sb.sleep(3)
