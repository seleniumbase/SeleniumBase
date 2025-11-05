from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.indeed.com/companies/search"
    sb.activate_cdp_mode(url)
    search_box = "input#company-search"
    if not sb.is_element_present(search_box):
        sb.sleep(2)
        sb.solve_captcha()
        sb.sleep(1)
    company = "NASA Jet Propulsion Laboratory"
    sb.click(search_box)
    sb.sleep(0.1)
    sb.press_keys(search_box, company)
    sb.click('button[type="submit"]')
    sb.click('a:contains("%s")' % company)
    name_header = 'div[itemprop="name"]'
    sb.sleep(1)
    if not sb.is_element_present(name_header):
        sb.sleep(2)
        sb.solve_captcha()
        sb.sleep(1)
    sb.highlight(name_header)
    sb.sleep(1)
    sb.cdp.highlight('h2:contains("About the company")')
    sb.sleep(1)
    for i in range(10):
        sb.scroll_down(12)
        sb.sleep(0.14)
    info = sb.find_element('[data-testid="AboutSection-section"]')
    soup = sb.get_beautiful_soup(info.get_html()).get_text("\n").strip()
    print("*** %s: ***\n%s" % (company, soup.replace("\n:", ":")))
