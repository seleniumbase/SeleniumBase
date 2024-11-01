"""Using CDP.network.ResponseReceived and CDP.network.RequestWillBeSent."""
import colorama
import mycdp
import sys
from seleniumbase import SB

c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""


async def send_handler(event: mycdp.network.RequestWillBeSent):
    r = event.request
    s = f"{r.method} {r.url}"
    for k, v in r.headers.items():
        s += f"\n\t{k} : {v}"
    print(c1 + "*** ==> RequestWillBeSent <== ***" + cr)
    print(s)


async def receive_handler(event: mycdp.network.ResponseReceived):
    print(c2 + "*** ==> ResponseReceived <== ***" + cr)
    print(event.response)


with SB(uc=True, test=True, locale_code="en") as sb:
    sb.activate_cdp_mode("about:blank")
    sb.cdp.add_handler(mycdp.network.RequestWillBeSent, send_handler)
    sb.cdp.add_handler(mycdp.network.ResponseReceived, receive_handler)
    url = "https://seleniumbase.io/apps/calculator"
    sb.cdp.open(url)
    sb.sleep(1)
