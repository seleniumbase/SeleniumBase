from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.clearcotelabs.com/audit")
sb.click('button:contains("Run the audit")')
sb.sleep(5)
sb.assert_element("div.text-emerald-700", timeout=6)
try:
    sb.assert_text("100", "div.text-emerald-700", timeout=5)
    sb.highlight('div.text-emerald-700:contains("100")')
    print(" ✅ The browser fingerprint is clean! Score: 100")
except Exception:
    score = sb.get_text("div.text-emerald-700")
    print(f" ❌ Fingerprint tampering detected! Score: {score}")
sb.sleep(1)
folder = "downloaded_files"
file_name = "c_audit_results.pdf"
sb.save_as_pdf(file_name, folder)
print('"./%s/%s" was saved!' % (folder, file_name))
sb.quit()
