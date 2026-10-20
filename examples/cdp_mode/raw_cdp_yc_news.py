"""Search Hacker News via Algolia"""
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(fast=True)
sb.goto("https://hn.algolia.com/?query=seleniumbase")
elements = sb.find_elements("div.Story_title > a")
for element in elements:
    print("* " + element.text)
