"""Search Hacker News via Algolia. Then print items and save to PDF."""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(fast=True)
sb.goto("https://hn.algolia.com/?query=seleniumbase")
elements = sb.find_elements("div.Story_title > a")
for element in elements:
    print("--> " + element.text)
sb.save_as_pdf("sb_news.pdf", folder="./downloaded_files/")
print("*** PDF saved to: ./downloaded_files/sb_news.pdf")
