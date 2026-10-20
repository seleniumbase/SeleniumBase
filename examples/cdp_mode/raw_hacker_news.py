"""Search Hacker News via Algolia"""
from seleniumbase import SB

with SB(uc=True, fast=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://hn.algolia.com/?query=seleniumbase")
    elements = sb.find_elements("div.Story_title > a")
    for element in elements:
        print("* " + element.text)
