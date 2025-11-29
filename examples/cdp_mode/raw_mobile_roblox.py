import mycdp
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.roblox.com/"
    agent = (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Mobile Safari/537.36"
    )
    sb.activate_cdp_mode(agent=agent)
    tab = sb.cdp.get_active_tab()
    loop = sb.cdp.get_event_loop()
    loop.run_until_complete(
        tab.send(
            mycdp.emulation.set_device_metrics_override(
                width=412, height=732, device_scale_factor=3, mobile=True
            )
        )
    )
    sb.open(url)
    sb.assert_element("#download-the-app-container")
    sb.assert_text("Roblox for Android")
    sb.highlight('span:contains("Roblox for Android")', loops=8)
    sb.highlight('span:contains("Continue in App")', loops=8)
