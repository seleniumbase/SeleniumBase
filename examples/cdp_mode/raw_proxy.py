from seleniumbase import decorators
from seleniumbase import sb_cdp

# Change this to "ip:port" or "user:pass@ip:port"
proxy = None


@decorators.print_runtime("CDP Proxy Example")
def main():
    url = "https://api.ipify.org/"
    sb = sb_cdp.Chrome(url, lang="en", pls="none", proxy=proxy)
    ip_address = sb.get_text("body")
    if "ERR" in ip_address:
        raise Exception("Failed to determine IP Address!")
    print("\n\nMy IP Address = %s\n" % ip_address)
    sb.open("https://ipinfo.io/%s" % ip_address)
    sb.sleep(2)
    sb.wait_for_text(ip_address, "h1", timeout=20)
    sb.find_element('[href="/signup"]')
    sb.wait_for_text("Hosted domains", timeout=20)
    sb.highlight("h1")
    pop_up = '[role="dialog"] span.cursor-pointer'
    sb.click_if_visible(pop_up)
    sb.highlight("#block-summary")
    sb.click_if_visible(pop_up)
    sb.highlight("#block-geolocation")
    sb.click_if_visible(pop_up)
    sb.sleep(2)
    print("Displaying Host Info:")
    text = sb.get_text("#block-summary").split("Hosted domains")[0]
    rows = text.split("\n")
    data = []
    for row in rows:
        if row.strip() != "":
            data.append(row.strip())
    print("\n".join(data).replace('\n"', ' "'))
    print("\nDisplaying GeoLocation Info:")
    text = sb.get_text("#block-geolocation")
    text = text.split("IP Geolocation data")[0]
    rows = text.split("\n")
    data = []
    for row in rows:
        if row.strip() != "":
            data.append(row.strip())
    print("\n".join(data).replace('\n"', ' "'))
    sb.click_if_visible(pop_up)
    sb.sleep(3)
    sb.driver.stop()


if __name__ == "__main__":
    main()
