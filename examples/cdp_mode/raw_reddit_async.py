import asyncio
from seleniumbase import cdp_driver


async def main():
    search = "Reddit Scraping"
    driver = await cdp_driver.start_async(use_chromium=True)
    page = await driver.get("https://www.reddit.com/r/webscraping/")
    await page.solve_captcha()  # Might not be needed
    element = await page.find("faceplate-search-input")
    await element.mouse_click_async()
    await page.type("html", search + "\n")
    await page.sleep(2.5)
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
    asyncio.run(main())
