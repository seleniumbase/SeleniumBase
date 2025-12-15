from seleniumbase import sb_cdp

url = "https://copilot.microsoft.com/"
sb = sb_cdp.Chrome(url, locale="en", guest=True)
textarea = "textarea#userInput"
sb.wait_for_element(textarea)
sb.sleep(1.3)
sb.click_if_visible('[aria-label="Dismiss"]')
sb.sleep(0.5)
sb.click('button[data-testid*="chat-mode-"]')
sb.sleep(1.1)
sb.click_if_visible('button[title^="Think"]')
sb.sleep(1.1)
query = "How to start automating with SeleniumBase?"
sb.press_keys(textarea, query)
sb.sleep(1.1)
seen_text = sb.get_text(textarea)
if seen_text != query and seen_text in query:
    # When CAPTCHA appears while typing text
    sb.sleep(1.1)
    sb.solve_captcha()
    sb.sleep(2.2)
    sb.type(textarea, "")
    sb.press_keys(textarea, query)
    sb.sleep(0.5)
sb.click('button[data-testid="submit-button"]')
sb.sleep(2.5)
sb.solve_captcha()
sb.sleep(3.5)
sb.solve_captcha()
sb.sleep(2.5)
stop_button = '[data-testid="stop-button"]'
thumbs_up = 'button[data-testid*="-thumbs-up-"]'
sb.wait_for_element_absent(stop_button, timeout=50)
sb.wait_for_element(thumbs_up, timeout=20)
sb.sleep(0.6)
scroll = 'button[data-testid*="scroll-to-bottom"]'
sb.click_if_visible(scroll)
sb.sleep(2.2)
folder = "downloaded_files"
file_name = "copilot_results.html"
sb.save_as_html(file_name, folder)
print('"./%s/%s" was saved!' % (folder, file_name))
sb.driver.stop()
