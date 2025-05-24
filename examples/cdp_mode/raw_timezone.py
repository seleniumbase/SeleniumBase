"""Timezone example using CDP Mode without WebDriver"""
import mycdp
from seleniumbase import decorators
from seleniumbase import sb_cdp


async def request_paused_handler(event, tab):
    r = event.request
    is_image = ".png" in r.url or ".jpg" in r.url or ".gif" in r.url
    if not is_image:  # Let the data through
        tab.feed_cdp(mycdp.fetch.continue_request(request_id=event.request_id))
    else:  # Block the data (images)
        TIMED_OUT = mycdp.network.ErrorReason.TIMED_OUT
        tab.feed_cdp(mycdp.fetch.fail_request(event.request_id, TIMED_OUT))


@decorators.print_runtime("Timezone CDP Example")
def main():
    url = "https://www.randymajors.org/what-time-zone-am-i-in"
    sb = sb_cdp.Chrome(
        url,
        ad_block=True,
        lang="bn",
        tzone="Asia/Kolkata",
        geoloc=(26.855323, 80.937710)
    )
    sb.add_handler(mycdp.fetch.RequestPaused, request_paused_handler)
    sb.remove_elements("#right-sidebar")
    sb.remove_elements('[id*="Footer"]')
    sb.sleep(6)
    sb.driver.stop()


if __name__ == "__main__":
    main()
