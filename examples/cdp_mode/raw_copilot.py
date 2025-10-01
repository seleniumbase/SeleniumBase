from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    url = "https://copilot.microsoft.com/"
    sb.activate_cdp_mode(url)
    textarea = "textarea#userInput"
    sb.wait_for_element(textarea)
    sb.sleep(1.5)
    sb.click_if_visible('[aria-label="Dismiss"]')
    sb.sleep(0.5)
    sb.click('button[data-testid*="chat-mode-"]')
    sb.sleep(1.1)
    sb.click('button[title="Think Deeper"]')
    sb.sleep(1.1)
    query = "How to migrate from Playwright to SeleniumBase?"
    sb.press_keys(textarea, query)
    sb.sleep(1.1)
    sb.click('button[data-testid="submit-button"]')
    sb.sleep(2.5)
    sb.uc_gui_click_captcha()
    sb.sleep(2.5)
    sb.uc_gui_click_captcha()
    sb.sleep(2.5)
    stop_button = '[data-testid="stop-button"]'
    thumbs_up = 'button[data-testid*="-thumbs-up-"]'
    sb.wait_for_element_absent(stop_button, timeout=30)
    sb.wait_for_element(thumbs_up, timeout=30)
    sb.sleep(0.5)
    sb.click('button[data-testid*="scroll-to-bottom"]')
    sb.sleep(1.5)
    folder = "downloaded_files"
    file_name = "copilot_results.html"
    sb.save_page_source(file_name, folder)
    print('"./%s/%s" was saved!' % (folder, file_name))
