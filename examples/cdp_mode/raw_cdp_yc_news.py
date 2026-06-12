from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://news.ycombinator.com/submitted?id=seleniumbase")
elements = sb.find_elements("span.titleline > a")
for element in elements:
    print("* " + element.text)
