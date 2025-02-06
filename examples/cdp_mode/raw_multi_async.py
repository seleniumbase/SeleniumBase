# Testing multiple CDP drivers using the async API
import asyncio
from concurrent.futures import ThreadPoolExecutor
from random import randint
from seleniumbase.undetected import cdp_driver


async def main(url):
    driver = await cdp_driver.cdp_util.start_async()
    page = await driver.get(url)
    await page.set_window_rect(randint(4, 600), randint(8, 410), 860, 500)
    await page.sleep(0.5)
    field = await page.select("input")
    await field.send_keys_async("Text")
    button = await page.select("button")
    await button.click_async()
    await page.sleep(2)


def set_up_loop(url):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(url))


if __name__ == "__main__":
    urls = ["https://seleniumbase.io/demo_page" for i in range(4)]
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        for url in urls:
            executor.submit(set_up_loop, url)
