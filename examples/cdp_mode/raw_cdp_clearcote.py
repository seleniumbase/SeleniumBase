from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.clearcotelabs.com/audit")
sb.click('button[aria-label="Marker 1"]')
sb.click('button[aria-label="Marker 2"]')
sb.click('button[aria-label="Marker 3"]')
sb.press_keys("input", "audit")
sb.set_value('input[type="range"]', "100")
sb.select_option_by_text("select", "Mouse")
sb.click('button:contains("Run the audit")')
sb.sleep(6)
sb.assert_element("div.text-successText", timeout=8)
try:
    sb.assert_text("100", "div.text-successText", timeout=5)
    sb.highlight('div.text-successText:contains("100")')
    print(" ✅ The browser fingerprint is clean! Score: 100")
except Exception:
    score = sb.get_text("div.text-successText")
    print(f" ❌ Fingerprint tampering detected! Score: {score}")
sb.sleep(1)
folder = "downloaded_files"
file_name = "c_audit_results.pdf"
sb.save_as_pdf(file_name, folder)
print('"./%s/%s" was saved!' % (folder, file_name))
sb.quit()
