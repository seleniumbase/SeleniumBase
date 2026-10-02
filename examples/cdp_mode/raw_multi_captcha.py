# Testing multiple CDP drivers using the sync API
from concurrent.futures import ThreadPoolExecutor
from random import randint
from seleniumbase import decorators
from seleniumbase import sb_cdp


def main(url):
    sb = sb_cdp.Chrome()
    sb.goto(url)
    sb.set_window_rect(randint(4, 680), randint(8, 380), 840, 520)
    sb.sleep(1.2)
    sb.solve_captcha()
    sb.sleep(2.2)
    sb.quit()


if __name__ == "__main__":
    urls = ["https://www.bing.com/turing/captcha/challenge" for i in range(4)]
    with decorators.print_runtime("raw_multi_captcha.py"):
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            for url in urls:
                executor.submit(main, url)
