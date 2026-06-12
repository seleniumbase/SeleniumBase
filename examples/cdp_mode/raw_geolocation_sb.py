"""Geolocation example with CDP Mode"""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    location = (31.774390, 35.222450)
    sb.activate_cdp_mode(geoloc=location)
    sb.goto("https://www.openstreetmap.org/")
    sb.click('a[aria-label="Show My Location"]')
    sb.assert_url_contains("31.774390/35.222450")
    sb.sleep(5)
