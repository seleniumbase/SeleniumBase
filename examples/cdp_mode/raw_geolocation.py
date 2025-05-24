"""Geolocation example using CDP Mode without WebDriver"""
from seleniumbase import decorators
from seleniumbase import sb_cdp


@decorators.print_runtime("Geolocation CDP Example")
def main():
    url = "https://www.openstreetmap.org/"
    sb = sb_cdp.Chrome(url, geoloc=(48.87645, 2.26340))
    sb.sleep(2)
    sb.click('a[aria-label="Show My Location"]')
    sb.assert_url_contains("48.876450/2.263400")
    sb.sleep(5)
    sb.driver.stop()


if __name__ == "__main__":
    main()
