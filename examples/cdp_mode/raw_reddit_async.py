import asyncio
from seleniumbase import cdp_driver


async def main():
    search = "reddit+scraper"
    url = f"https://www.reddit.com/r/webscraping/search/?q={search}"
    driver = await cdp_driver.start_async(use_chromium=True)
    page = await driver.get(url)
    await page.solve_captcha()  # Might not be needed
    post_title = '[data-testid="post-title"]'
    await page.select(post_title)
    for i in range(8):
        await page.scroll_down(25)
        await page.sleep(0.2)
    posts = await page.select_all(post_title)
    print('*** Reddit Posts for "%s":' % search)
    for post in posts:
        print("* " + post.text)
    driver.stop()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
