from seleniumbase import SB

with SB(uc=True) as sb:
    url = "https://news.ycombinator.com/submitted?id=seleniumbase"
    sb.activate_cdp_mode(url)
    elements = sb.find_elements("span.titleline > a")
    for element in elements:
        print("* " + element.text)
