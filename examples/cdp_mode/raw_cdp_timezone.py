from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(ad_block=True, incognito=True)
url = "https://www.randymajors.org/what-time-zone-am-i-in"
sb.goto(url, tzone="Asia/Kolkata", geoloc=(26.863, 80.94))
sb.remove_elements("#right-sidebar")
sb.sleep(2.5)
sb.remove_elements('[data-google-query-id]')
sb.remove_elements("iframe:not(#embedMapFrame)")
sb.sleep(2.5)
sb.goto(url, tzone="Asia/Tokyo", geoloc=(35.050681, 136.844728))
sb.remove_elements("#right-sidebar")
sb.sleep(2.5)
sb.remove_elements('[data-google-query-id]')
sb.remove_elements("iframe:not(#embedMapFrame)")
sb.sleep(2.5)
