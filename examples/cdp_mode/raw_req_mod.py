"""Using CDP.fetch.RequestPaused to modify requests in real-time."""
import mycdp
from seleniumbase import SB


async def request_paused_handler(event, tab):
    r = event.request
    is_image = ".png" in r.url or ".jpg" in r.url or ".gif" in r.url
    if not is_image:  # Let the data through
        tab.feed_cdp(mycdp.fetch.continue_request(request_id=event.request_id))
    else:  # Modify the data (change the image)
        tab.feed_cdp(mycdp.fetch.continue_request(
            request_id=event.request_id,
            url="https://seleniumbase.io/other/with_frakes.jpg"
        ))


with SB(uc=True, test=True, locale_code="en", pls="none") as sb:
    sb.activate_cdp_mode("about:blank")
    sb.cdp.add_handler(mycdp.fetch.RequestPaused, request_paused_handler)
    sb.cdp.open("https://gettyimages.com/photos/jonathan-frakes-cast-2022")
    new_size = "--width:100;--height:100;"
    sb.cdp.set_attributes('[style*="--width:"]', "style", new_size)
    sb.sleep(6)
