import json
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://quotes.toscrape.com/")
all_quotes = []
while True:
    quotes = sb.find_elements("div.quote")
    for quote in quotes:
        all_quotes.append(
            {
                "author": quote.query_selector("span small").text,
                "text": quote.query_selector("span.text").text,
            }
        )
    if sb.is_element_visible("li.next"):
        sb.click("li.next")
    else:
        break
file_path = "downloaded_files/quotes.json"
with open(file_path, "w", encoding="utf-8") as outfile:
    json.dump(all_quotes, outfile)
print(f'Quotes saved to "{file_path}".')
sb.quit()
