"""An example of changing settings during CDP Mode"""
from seleniumbase import SB

with SB(uc=True, test=True, pls="eager", ad_block=True) as sb:
    url = "https://www.randymajors.org/what-time-zone-am-i-in"
    sb.activate_cdp_mode(url, tzone="Asia/Kolkata", geoloc=(26.863, 80.94))
    sb.remove_elements("#right-sidebar")
    sb.sleep(5)
    sb.cdp.open(url, tzone="Asia/Tokyo", geoloc=(35.050681, 136.844728))
    sb.remove_elements("#right-sidebar")
    sb.sleep(5)
