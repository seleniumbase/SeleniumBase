from seleniumbase import SB

with SB(uc=True, test=True, use_chromium=True, incognito=True) as sb:
    sb.goto("https://www.indeed.com/?from=gnav-compui")
    sb.sleep(0.6)
    search = "AI Engineer"
    sb.type('input[name="q"]', search)
    sb.click('button[type="submit"]')
    sb.sleep(3.6)
    items = sb.find_visible_elements('[data-testid*="jobcard"]')
    print('*** Indeed search for "%s":' % search)
    for i, item in enumerate(items):
        print(f"* <====== {i + 1} ======>")
        print(item.text)
        item.scroll_into_view()
    print(f"*** {len(items)} total items found!")
