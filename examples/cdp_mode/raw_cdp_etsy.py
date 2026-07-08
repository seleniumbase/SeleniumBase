from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(ad_block=True)
sb.goto("https://www.etsy.com/")
sb.sleep(1)
search = "FIFA Keychains"
required_text = "keychain"
sb.type('input[data-id="search-query"]', search)
sb.sleep(1)
sb.click('button[aria-label="Search"]')
sb.sleep(2)
sb.click_if_visible('button[aria-label="Ok"]')
soup = sb.get_beautiful_soup()
items = soup.select("div.v2-listing-card__info")
num = 0
for item in items:
    title_element = item.select_one("h3.v2-listing-card__title")
    price_element = item.select_one("div.n-listing-card__price")
    if title_element and price_element:
        title = title_element.get_text()
        price = price_element.get_text()
        if required_text.lower() in title.lower():
            num += 1
            title = " ".join(title.split()).strip()
            price = price.replace("Sale Price", "").strip().split("\n")[0]
            print(f"* <====== {num} ======>")
            print(title)
            print(price.strip().split("\n")[0])
print(f"*** {num} total items found!")
