import json
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.yelp.com/")
sb.sleep(3)
restaurants_menu = 'button[aria-label*="Restaurants"]'
cafes = 'span:contains("Cafes")'
sb.wait_for_element(restaurants_menu)
sb.sleep(1)
sb.hover_and_click(restaurants_menu, cafes)
sb.sleep(3)
all_cafes = []
counter = 0
max_pages = 3
while True:
    dtci = '[data-traffic-crawl-id="SearchResult%s"]'
    cafes = sb.find_elements('[data-testid="serp-ia-card"]')
    for cafe in cafes:
        name = cafe.query_selector(dtci % "BizName")
        rating = cafe.query_selector(dtci % "BizRating")
        snippet = cafe.query_selector(dtci % "ReviewSnippet")
        if name and rating and snippet:
            all_cafes.append(
                {
                    "name": name.text,
                    "rating": rating.text,
                    "snippet": snippet.text,
                }
            )
    counter += 1
    if counter >= max_pages:
        break
    if sb.is_element_visible('span:contains("Next Page")'):
        sb.click('span:contains("Next Page")')
        sb.sleep(1)
    else:
        break
file_path = "downloaded_files/cafes.json"
with open(file_path, "w", encoding="utf-8") as outfile:
    json.dump(all_cafes, outfile)
print(f'Cafes saved to "{file_path}".')
sb.quit()
