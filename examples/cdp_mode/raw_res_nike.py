"""Using CDP.network.RequestWillBeSent and CDP.network.ResponseReceived."""
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


with SB(uc=True, test=True, locale="en", pls="none") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.cdp.add_handler(mycdp.network.RequestWillBeSent, send_handler)
    sb.cdp.add_handler(mycdp.network.ResponseReceived, receive_handler)
    sb.sleep(2.5)
    sb.cdp.click('div[data-testid="user-tools-container"]')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.cdp.press_keys('input[type="search"]', search)
    sb.sleep(4)
    elements = sb.cdp.select_all('ul[data-testid*="products"] figure .details')
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
    sb.sleep(2)
