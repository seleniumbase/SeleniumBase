from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.softpedia.com/"
    sb.activate_cdp_mode(url)
    search_box = 'input[name="search_term"]'
    search = "3D Model Lab"
    sb.click(search_box)
    sb.press_keys(search_box, search + "\n")
    sb.sleep(2)
    sb.remove_elements("#adcontainer1")
    sb.sleep(2.5)
    print('*** Softpedia Search for "%s":' % search)
    links = []
    item_container = 'div[style="min-height:100px;"]'
    sb.wait_for_element(item_container)
    items = sb.find_elements(item_container)
    for item in items:
        result = item.querySelector("h4 a")
        links.append(result.get_attribute("href"))
        print("* " + result.text)
        print(item.querySelector("p").get_attribute("title"))
    for link in links:
        sb.open(link)
        sb.remove_elements("div.ad")
        sb.sleep(2)
