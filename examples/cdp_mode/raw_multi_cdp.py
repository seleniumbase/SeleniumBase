# Testing multiple CDP drivers using the sync API
import asyncio
from concurrent.futures import ThreadPoolExecutor
from random import randint
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


def main(url):
    loop = asyncio.new_event_loop()
    driver = cdp_driver.cdp_util.start_sync()
    page = loop.run_until_complete(driver.get(url))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.set_window_rect(randint(4, 720), randint(8, 410), 800, 500)
    sb.press_keys("input", "Text")
    sb.highlight("button")
    sb.click("button")
    sb.sleep(2)


if __name__ == "__main__":
    urls = ["https://seleniumbase.io/demo_page" for i in range(4)]
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        for url in urls:
            executor.submit(main, url)
