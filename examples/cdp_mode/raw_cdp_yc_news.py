from seleniumbase import sb_cdp

url = "https://news.ycombinator.com/submitted?id=seleniumbase"
sb = sb_cdp.Chrome(url)
elements = sb.find_elements("span.titleline > a")
for element in elements:
    print("* " + element.text)
sb.driver.stop()
