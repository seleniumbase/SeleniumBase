# Testing multiple CDP drivers using the async API
import asyncio
from concurrent.futures import ThreadPoolExecutor
from random import randint
from seleniumbase import cdp_driver
from seleniumbase import decorators


async def main(url):
    driver = await cdp_driver.start_async()
    page = await driver.get(url)
    await page.set_window_rect(randint(4, 600), randint(8, 410), 860, 500)
    await page.sleep(0.5)
    await page.type("input", "Text")
    await page.click("button")
    await page.sleep(2)
    driver.stop()


def set_up_loop(url):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(url))


if __name__ == "__main__":
    urls = ["https://seleniumbase.io/demo_page" for i in range(5)]
    with decorators.print_runtime("raw_multi_async.py"):
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            for url in urls:
                executor.submit(set_up_loop, url)
