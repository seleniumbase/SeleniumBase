"""Using CDP.fetch.RequestPaused to filter content in real-time."""
import colorama
import mycdp
import sys
from seleniumbase import SB

c1 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""


async def request_paused_handler(event, tab):
    r = event.request
    is_image = ".png" in r.url or ".jpg" in r.url or ".gif" in r.url
    if not is_image:  # Let the data through
        tab.feed_cdp(mycdp.fetch.continue_request(request_id=event.request_id))
    else:  # Block the data (images)
        TIMED_OUT = mycdp.network.ErrorReason.TIMED_OUT
        s = f"{c1}BLOCKING{cr} | {c2}{r.method}{cr} | {r.url}"
        print(f" >>> ------------\n{s}")
        tab.feed_cdp(mycdp.fetch.fail_request(event.request_id, TIMED_OUT))


with SB(uc=True, test=True, locale_code="en") as sb:
    sb.activate_cdp_mode("about:blank")
    sb.cdp.add_handler(mycdp.fetch.RequestPaused, request_paused_handler)
    url = "https://gettyimages.com/photos/firefly-2003-nathan"
    sb.cdp.open(url)
    sb.sleep(5)
