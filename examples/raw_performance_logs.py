from rich.pretty import pprint
from seleniumbase import SB

with SB(log_cdp=True) as sb:
    sb.goto("seleniumbase.io/demo_page")
    sb.sleep(1)
    pprint(sb.driver.get_log("performance"))
