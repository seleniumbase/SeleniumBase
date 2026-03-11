import mycdp
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.activate_cdp_mode("https://learn.microsoft.com/en-us/")
    tab = sb.cdp.get_active_tab()
    loop = sb.cdp.get_event_loop()
    print(loop.run_until_complete(tab.send(mycdp.storage.get_cookies())))
