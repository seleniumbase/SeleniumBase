# Testing multiple CDP drivers using the sync API
from concurrent.futures import ThreadPoolExecutor
from random import randint
from seleniumbase import decorators
from seleniumbase import sb_cdp


def main(url):
    sb = sb_cdp.Chrome(url, lang="en")
    sb.set_window_rect(randint(4, 680), randint(8, 380), 840, 520)
    sb.sleep(2)
    sb.gui_click_captcha()
    sb.sleep(2)
    sb.driver.quit()


if __name__ == "__main__":
    urls = ["https://seleniumbase.io/apps/turnstile" for i in range(5)]
    with decorators.print_runtime("raw_multi_captcha.py"):
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            for url in urls:
                executor.submit(main, url)
