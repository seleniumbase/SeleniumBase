"""Using CDP.fetch.RequestPaused to filter content in real time."""
import mycdp
from seleniumbase import SB


async def request_paused_handler(event, tab):
    r = event.request
    is_image = ".png" in r.url or ".jpg" in r.url or ".gif" in r.url
    is_blocked = True if is_image else False
    if not is_blocked:
        tab.feed_cdp(mycdp.fetch.continue_request(request_id=event.request_id))
    else:
        TIMED_OUT = mycdp.network.ErrorReason.TIMED_OUT
        s = f"BLOCKING | {r.method} | {r.url}"
        print(f" >>> ------------\n{s}")
        tab.feed_cdp(mycdp.fetch.fail_request(event.request_id, TIMED_OUT))


with SB(uc=True, test=True, locale_code="en", incognito=True) as sb:
    sb.activate_cdp_mode("about:blank")
    sb.cdp.add_handler(mycdp.fetch.RequestPaused, request_paused_handler)
    url = "https://gettyimages.com/photos/firefly-2003-nathan"
    sb.cdp.open(url)
    sb.sleep(5)
