import mycdp
from seleniumbase import decorators
from seleniumbase import sb_cdp


async def block_urls(tab):
    await tab.send(mycdp.network.enable())
    await tab.send(mycdp.network.set_blocked_urls(
        urls=[
            "*.googlesyndication.com*",
            "*.googletagmanager.com*",
            "*.google-analytics.com*",
            "*.amazon-adsystem.com*",
            "*.adsafeprotected.com*",
            "*.doubleclick.net*",
            "*.fastclick.net*",
            "*.snigelweb.com*",
            "*.2mdn.net*",
        ]
    ))

with decorators.print_runtime("raw_ad_blocking.py"):
    sb = sb_cdp.Chrome()
    loop = sb.get_event_loop()
    loop.run_until_complete(block_urls(sb.get_active_tab()))
    sb.open("https://www.w3schools.com/jquery/default.asp")
    source = sb.get_page_source()
    sb.assert_true("doubleclick.net" not in source)
    sb.assert_true("google-analytics.com" not in source)
    sb.post_message("Blocking was successful!")
    sb.driver.quit()
