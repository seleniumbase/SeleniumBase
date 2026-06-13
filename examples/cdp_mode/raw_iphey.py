from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://iphey.com")
    sb.sleep(7)
    trustworthy = "#hero-status"
    sb.assert_element(trustworthy)
    sb.assert_text("Trustworthy", trustworthy)
    sb.highlight(trustworthy, loops=10, scroll=False)
    items = sb.find_elements('a[style*="check-circle"]')
    sb.assert_true(len(items) == 5, "Expecting 5 checks!")
    for item in items:
        item.flash(color="44CC88")
        sb.sleep(0.2)
    sb.sleep(2)
    sb.save_screenshot_to_logs()
