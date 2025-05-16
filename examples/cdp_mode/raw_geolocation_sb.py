"""Geolocation example with CDP Mode"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.openstreetmap.org/"
    sb.activate_cdp_mode(url, geoloc=(31.774390, 35.222450))
    sb.click('a[aria-label="Show My Location"]')
    sb.assert_url_contains("31.774390/35.222450")
    sb.sleep(5)
