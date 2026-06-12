from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://news.ycombinator.com/submitted?id=seleniumbase")
    elements = sb.find_elements("span.titleline > a")
    for element in elements:
        print("* " + element.text)
