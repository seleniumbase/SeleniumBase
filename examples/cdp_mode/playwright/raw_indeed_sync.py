from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.open("https://www.indeed.com/companies/search")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    search_box = "input#company-search"
    if page.locator(search_box).count() == 0:
        page.wait_for_timeout(2500)
        sb.solve_captcha()
        page.wait_for_timeout(1000)
    company = "NASA Jet Propulsion Laboratory"
    page.click(search_box)
    page.fill(search_box, company)
    page.click('button[type="submit"]')
    page.click('a:has-text("%s")' % company)
    name_header = 'div[itemprop="name"]'
    page.wait_for_timeout(1000)
    if page.locator(name_header).count() == 0:
        page.wait_for_timeout(2500)
        sb.solve_captcha()
        page.wait_for_timeout(1000)
    for i in range(10):
        sb.scroll_down(12)
        sb.sleep(0.14)
    info = page.locator('[data-testid="AboutSection-section"]')
    soup = sb.get_beautiful_soup(info.inner_html()).get_text("\n")
    print("*** %s: ***\n%s" % (company, soup))
